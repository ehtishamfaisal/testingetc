# -*- coding: utf-8 -*-

import base64

import werkzeug
import werkzeug.urls

from odoo import http, SUPERUSER_ID
from odoo.http import request
import time
from odoo.addons.website.models.website import slug

from odoo.tools.translate import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main

main.PPG = 18
PPG=main.PPG
PPR = 4   # Products Per Row


class WebsiteSale(WebsiteSale):

    @http.route([
        '/shop/benches',
        '/shop/benches/page/<int:page>',
        '/shop/benches/category/<model("product.public.category"):category>',
        '/shop/benches/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def benches(self, page=0, category=None, search='', wk_price=None, ppg=False, **post):
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category:
                raise NotFound()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop/benches', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        
#Price Attribute =====================================================
        attrib_prices = request.httprequest.args.getlist('attrib_price')
        price_set=[]
        brand =(post.get('brand')  and post.get('brand')) or False
        for attrib_price in attrib_prices:
            attrib_price_index = attrib_price.split('-')[0]
            if brand:
                if (brand!=attrib_price_index):
                    price_set+=[int(attrib_price_index)]
            else:
                price_set+=[int(attrib_price_index)]
        price_set = list(set(price_set))
        price_rec = request.env['wk.product.price'].search([])
        wk_price = request.env['wk.product.price'].browse(list(set(price_set)))

#Leg Style Attribute =====================================================
        att_leg_style = request.httprequest.args.getlist('att_leg_style')
        set_leg_style = [int(x.encode('UTF8')) for x in att_leg_style]
        leg_style = request.env['leg.style'].search([])
        
#Leg Style Attribute =====================================================
        att_table_style = request.httprequest.args.getlist('att_table_style')
        set_table_style = [int(x.encode('UTF8')) for x in att_table_style]
        table_style = request.env['table.style'].search([])

        url = "/shop/benches"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        categs = request.env['product.public.category'].search([('parent_id', '=', False)])
        Product = request.env['product.template']
        domain += [('wk_type','=','b')]
        parent_category_ids = []
        if category:
            url = "/shop/benches/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
    
        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'wk_price':wk_price, 'price_rec':price_rec, 'price_set':price_set,
            'set_leg_style':set_leg_style,'leg_style':leg_style,
            'set_table_style':set_table_style,'table_style':table_style,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)
    
    
    @http.route([
        '/shop/dining/tables',
        '/shop/dining/tables/page/<int:page>',
        '/shop/dining/tables/category/<model("product.public.category"):category>',
        '/shop/dining/tables/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def DiningTables(self, page=0, category=None, search='', wk_price=None, ppg=False, **post):
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category:
                raise NotFound()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop/dining/tables', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

#Price Attribute =====================================================
        attrib_prices = request.httprequest.args.getlist('attrib_price')
        price_set=[]
        brand =(post.get('brand')  and post.get('brand')) or False
        for attrib_price in attrib_prices:
            attrib_price_index = attrib_price.split('-')[0]
            if brand:
                if (brand!=attrib_price_index):
                    price_set+=[int(attrib_price_index)]
            else:
                price_set+=[int(attrib_price_index)]
        price_set = list(set(price_set))
        price_rec = request.env['wk.product.price'].search([])
        wk_price = request.env['wk.product.price'].browse(list(set(price_set)))
        
#Leg Style Attribute =====================================================
        att_leg_style = request.httprequest.args.getlist('att_leg_style')
        set_leg_style = [int(x.encode('UTF8')) for x in att_leg_style]
        leg_style = request.env['leg.style'].search([])
        
#Leg Style Attribute =====================================================
        att_table_style = request.httprequest.args.getlist('att_table_style')
        set_table_style = [int(x.encode('UTF8')) for x in att_table_style]
        table_style = request.env['table.style'].search([])

        url = "/dining/tables"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        categs = request.env['product.public.category'].search([('parent_id', '=', False)])
        Product = request.env['product.template']
        domain += [('wk_type','=','dt')]
        parent_category_ids = []
        if category:
            url = "/shop/dining/tables/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'wk_price':wk_price, 'price_rec':price_rec, 'price_set':price_set,
            'set_leg_style':set_leg_style,'leg_style':leg_style,
            'set_table_style':set_table_style,'table_style':table_style,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)
    
    
    @http.route([
        '/shop/dining/set/tables',
        '/shop/dining/set/tables/page/<int:page>',
        '/shop/dining/set/tables/category/<model("product.public.category"):category>',
        '/shop/dining/set/tables/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def SetTables(self, page=0, category=None, search='', wk_price=None, ppg=False, **post):
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG

        if category:
            category = request.env['product.public.category'].search([('id', '=', int(category))], limit=1)
            if not category:
                raise NotFound()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [map(int, v.split("-")) for v in attrib_list if v]
        attributes_ids = set([v[0] for v in attrib_values])
        attrib_set = set([v[1] for v in attrib_values])

        domain = self._get_search_domain(search, category, attrib_values)

        keep = QueryURL('/shop/dining/set/tables', category=category and int(category), search=search, attrib=attrib_list, order=post.get('order'))
        pricelist_context = dict(request.env.context)
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])

        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

#Price Attribute =====================================================
        attrib_prices = request.httprequest.args.getlist('attrib_price')
        price_set=[]
        brand =(post.get('brand')  and post.get('brand')) or False
        for attrib_price in attrib_prices:
            attrib_price_index = attrib_price.split('-')[0]
            if brand:
                if (brand!=attrib_price_index):
                    price_set+=[int(attrib_price_index)]
            else:
                price_set+=[int(attrib_price_index)]
        price_set = list(set(price_set))
        price_rec = request.env['wk.product.price'].search([])
        wk_price = request.env['wk.product.price'].browse(list(set(price_set)))

#Leg Style Attribute =====================================================
        att_leg_style = request.httprequest.args.getlist('att_leg_style')
        set_leg_style = [int(x.encode('UTF8')) for x in att_leg_style]
        leg_style = request.env['leg.style'].search([])
        
#Leg Style Attribute =====================================================
        att_table_style = request.httprequest.args.getlist('att_table_style')
        set_table_style = [int(x.encode('UTF8')) for x in att_table_style]
        table_style = request.env['table.style'].search([])
        
        url = "/shop/dining/set/tables"
        if search:
            post["search"] = search
        if attrib_list:
            post['attrib'] = attrib_list

        categs = request.env['product.public.category'].search([('parent_id', '=', False)])
        Product = request.env['product.template']
        domain += [('wk_type','=','dts')]
        parent_category_ids = []
        if category:
            url = "/shop/dining/set/tables/category/%s" % slug(category)
            parent_category_ids = [category.id]
            current_category = category
            while current_category.parent_id:
                parent_category_ids.append(current_category.parent_id.id)
                current_category = current_category.parent_id

        product_count = Product.search_count(domain)
        pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
        products = Product.search(domain, limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        ProductAttribute = request.env['product.attribute']
        if products:
            # get all products without limit
            selected_products = Product.search(domain, limit=False)
            attributes = ProductAttribute.search([('attribute_line_ids.product_tmpl_id', 'in', selected_products.ids)])
        else:
            attributes = ProductAttribute.browse(attributes_ids)

        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)

        values = {
            'search': search,
            'category': category,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'pager': pager,
            'pricelist': pricelist,
            'products': products,
            'search_count': product_count,  # common for all searchbox
            'bins': TableCompute().process(products, ppg),
            'rows': PPR,
            'categories': categs,
            'attributes': attributes,
            'compute_currency': compute_currency,
            'keep': keep,
            'parent_category_ids': parent_category_ids,
            'wk_price':wk_price, 'price_rec':price_rec, 'price_set':price_set,
            'set_leg_style':set_leg_style,'leg_style':leg_style,
            'set_table_style':set_table_style,'table_style':table_style,
        }
        if category:
            values['main_object'] = category
        return request.render("website_sale.products", values)


