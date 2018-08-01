from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.http import request
from odoo import SUPERUSER_ID
from odoo import http

class WebsiteSale(WebsiteSale):
    
    
    @http.route(['/shop/get_products_content'], type='http', auth='public', website=True)
    def get_products_content(self, **post):
        cr,uid,context=request.cr,request.uid,request.context
        prod_ids=[]
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)

        value = {'products': False, 'header': False,'auto_scroll':False,'show_cart':False,'show_product_price':False,'show_product_name':False,'scroll_speed':False}
        if post.get('product_count') and post.get('slider_type'):
            if post.get('slider_type')=='is_arrival':
                prod_ids = request.env['product.template'].search([("sale_ok", "=", True)],order="id desc", limit=int(post.get('product_count')))
                if prod_ids:
                    prod_ids = prod_ids.ids            
            elif post.get('slider_type')=='is_latest_sale': 
                cr.execute("select product_id from sale_order_line order by id desc")
                product_ids=map(lambda x: x[0], cr.fetchall())
                if product_ids:
                    cr.execute("select distinct(product_product.product_tmpl_id) from product_product,product_template where product_product.id in %s and product_product.id=product_template.id and product_template.website_published='t'",(tuple(product_ids),))
                    prod_ids= map(lambda x: x[0], cr.fetchall())

            elif post.get('slider_type')=='is_best_saller': 
                cr.execute("select min(product_id)from sale_order_line group by product_id order by count(*) desc")
                product_ids=map(lambda x: x[0], cr.fetchall())
                if product_ids:
                    cr.execute("select distinct(product_product.product_tmpl_id) from product_product,product_template where product_product.id in %s and product_product.id=product_template.id and product_template.website_published='t'",(tuple(product_ids),))
                    prod_ids= map(lambda x: x[0], cr.fetchall())                         
            elif post.get('slider_type')=='is_discount': 
                cr.execute("select min(product_id)from sale_order_line group by product_id order by count(*) desc")
                product_ids=map(lambda x: x[0], cr.fetchall())
                if product_ids:
                    cr.execute("select distinct(product_product.product_tmpl_id) from product_product,product_template where product_product.id in %s and product_product.id=product_template.id and product_template.website_published='t'",(tuple(product_ids),))
                    prod_ids= map(lambda x: x[0], cr.fetchall())  
                    d_ids=[]
                    if prod_ids:
                        for datas in request.env['product.template'].browse(prod_ids):
                            if datas.lst_price>datas.price:
                                d_ids.append(datas.id)
                    prod_ids=d_ids 
            else:
                prod_ids=prod_ids.ids                                               
            if prod_ids:
                prod_ids=prod_ids
                prod_ids=prod_ids[:int(post.get('product_count'))]
                from_currency = request.env.user.company_id.currency_id
                to_currency = pricelist.currency_id
                compute_currency = lambda price: from_currency.compute(price, to_currency)                
                value.update({'compute_currency' : compute_currency})
                product_data = request.env['product.template'].browse(prod_ids)
                if product_data:
                    value['products'] = product_data
        if post.get('product_label'):
            value['header'] = post.get('product_label')
        if post.get('show_cart')=='true':
            value['show_cart']=True
        if post.get('auto_scroll')=='true':
            value['auto_scroll']=True
        if post.get('show_product_price')=='true':
            value['show_product_price']=True
        if post.get('show_product_name')=='true':
            value['show_product_name']=True 
        if post.get('scroll_speed'):
            value['scroll_speed']= post.get('scroll_speed') 
        if post.get('slider_id'):
             value['slider_id']= post.get('slider_id')
        return request.render("theme_watch.product_slider_content", value)
    
    
    @http.route(['/shop/get_product_brand_slider'], type='http', auth='public', website=True)
    def get_product_brand_slider(self, **post):
        value = {'header': False,'brands':False}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('brand-count'):
            brand_ids=request.env['product.brand'].search([('visible_slider','=',True)])
            if brand_ids:
                value.update({'brands':brand_ids})               
        return request.render("theme_watch.brand_slider_content", value)  


    @http.route(['/shop/get_multi_tab_content'], type='http', auth='public', website=True)
    def get_multi_tab_content(self, **post):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency)                
        value = {'obj': False,'compute_currency': compute_currency}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('collection_id'):
            collection_data=request.env['collection.configure'].browse(int(post.get('collection_id')))
            value.update({'obj':collection_data})
            return request.render("theme_watch.s_collection_configure", value)

        return ""

    @http.route(['/shop/multi_tab_product_snippet'], type='http', auth='public', website=True)
    def multi_tab_product_snippet(self, **post):
        pricelist_context = dict(request.env.context)
        pricelist = False
        if not pricelist_context.get('pricelist'):
            pricelist = request.website.get_current_pricelist()
            pricelist_context['pricelist'] = pricelist.id
        else:
            pricelist = request.env['product.pricelist'].browse(pricelist_context['pricelist'])
        request.context = dict(request.context, pricelist=pricelist.id, partner=request.env.user.partner_id)
        from_currency = request.env.user.company_id.currency_id
        to_currency = pricelist.currency_id
        compute_currency = lambda price: from_currency.compute(price, to_currency) 
        value = {'product_obj': False,'compute_currency': compute_currency}
        if post.get('label'):
            value['header'] = post.get('label')
        if post.get('collection_id'):
            collection_data=request.env['collection.configure'].browse(int(post.get('collection_id')))
            value.update({'product_obj':collection_data})
                
        return request.render("theme_watch.product_tab_content", value)

      
