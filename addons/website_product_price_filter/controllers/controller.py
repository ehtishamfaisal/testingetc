# -*- coding: utf-8 -*-
import werkzeug
import logging

from odoo import SUPERUSER_ID
from odoo import http

from odoo.addons.website_sale.controllers.main import WebsiteSale,PPG
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.website import slug

from odoo.exceptions import Warning
from odoo.http import request

_logger = logging.getLogger(__name__)

class WebsiteSale(WebsiteSale):
    
    
    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteSale, self).product(product=product, category=category, search=search, **kwargs)
        res.qcontext['finish'] = request.env['table.finish'].search([])
        print "res.qcontext",res.qcontext
        return res
    
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        print ">>>>>>>>>>>>>>>>>kw",kw
        res = request.website.sale_get_order(force_create=1)._cart_update(
            product_id=int(product_id),
            add_qty=add_qty,
            set_qty=set_qty,
            attributes=self._filter_attributes(**kw),
        )
        line_id = res.get('line_id', False)
        finish = kw.get('finish', False)
        if line_id and finish:
            line_id = request.env['sale.order.line'].browse(int(line_id))
            print "line_id",line_id.order_id
            line_id.finish_id = int(finish) 
        return request.redirect("/shop/cart")
    
    @http.route(
        ['/shop',
         '/shop/page/<int:page>',
         '/shop/category/<model("product.public.category"):category>',
         '/shop/category/<model("product.public.category"):category>/page/<int:page>'],
        type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False,wk_price=None,  **post):
        response= super(WebsiteSale, self).shop(page=page, category=category,
        search=search,wk_price=wk_price,ppg=ppg,**post)
#Price Attribute =====================================================
        brand =(post.get('brand')  and post.get('brand')) or False
        attrib_prices = request.httprequest.args.getlist('attrib_price')
        price_set=[]
        for attrib_price in attrib_prices:
            attrib_price_index = attrib_price.split('-')[0]
            if brand:
                if (brand!=attrib_price_index):
                    price_set+=[int(attrib_price_index)]
            else:
                price_set+=[int(attrib_price_index)]
                
        response.qcontext['price_set']= list(set(price_set))
        response.qcontext['price_rec']= request.env['wk.product.price'].search([])
        response.qcontext['wk_price']= request.env['wk.product.price'].browse(list(set(price_set)))

#Leg Style Attribute =====================================================
        att_leg_style = request.httprequest.args.getlist('att_leg_style')
        response.qcontext['set_leg_style'] = [int(x.encode('UTF8')) for x in att_leg_style]
        response.qcontext['leg_style'] = request.env['leg.style'].search([])
        
#Table Style Attribute =====================================================
        att_table_style = request.httprequest.args.getlist('att_table_style')
        response.qcontext['set_table_style'] = [int(x.encode('UTF8')) for x in att_table_style]
        response.qcontext['table_style'] = request.env['table.style'].search([])

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG
        qcontext = dict(response.qcontext)
        attrib_list = request.httprequest.args.getlist('attrib')
        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list
        search_count = len(qcontext.get('products'))
        pager = request.website.pager(url=url, total=qcontext.get('search_count'),
        page=page, step=ppg, scope=7, url_args=post)
        response.qcontext['pager'] = pager
        keep = QueryURL('/shop', category=category and int(category), search=search,
        attrib=attrib_list, order=post.get('order'),attrib_price=attrib_prices)
        response.qcontext['keep'] = keep
        return response
    

    def _get_search_domain(self, search, category, attrib_values):
        
        domain= super(WebsiteSale, self)._get_search_domain(search, category, attrib_values)
        domain = self._get_price_domain(domain, search, category, attrib_values)
        if request.httprequest.path == '/shop':
            domain += [('wk_type','=','ot')]
        return domain
    
    def _get_price_domain(self,domain,search, category, attrib_values):
        attrib_prices = request.httprequest.args.getlist('attrib_price')
        brand = request.httprequest.args.getlist('brand')
        price_set=[]
        for attrib_price in attrib_prices:
            attrib_price_index = attrib_price.split('-')[0]
            if brand:
                if brand[0]!=attrib_price_index:
                    price_set+=[int(attrib_price_index)]
            else:
                price_set+=[int(attrib_price_index)]
        if len(price_set):
            product_prices = request.env['wk.product.price'].browse(price_set)
            domain += [('list_price', '>=', product_prices[0].min_price), ('list_price', '<=', product_prices[-1].max_price)]
#Leg Style Domain ==========================================================
        att_leg_style = request.httprequest.args.getlist('att_leg_style')
        set_leg_style = [int(x.encode('UTF8')) for x in att_leg_style]
        if set_leg_style:
            domain += [('leg_style_ids','in',set_leg_style)]
        
#Table Style Domain ==========================================================
        att_table_style = request.httprequest.args.getlist('att_table_style')
        set_table_style = [int(x.encode('UTF8')) for x in att_table_style]
        if set_table_style:
            domain += [('table_style_ids','in',set_table_style)]
        return domain

