# -*- coding: utf-8 -*-

from openerp import api, fields, models, _
from openerp.exceptions import UserError
import openerp
from openerp.http import request
from openerp.addons.website.models.website import slugify


class website(models.Model):

    """Adds the fields for breadcum."""

    _inherit = 'website'

    bread_cum_image = fields.Binary(string="Breadcrumb Image")
    is_breadcum = fields.Boolean(string="Do you want to disable Breadcrumb?")

    @api.model
    def get_category_breadcum(self,category):
        data=[]
        parent_categ=False
        if category:
            categ_data=self.env['product.public.category'].search([('id','=',int(category))])
            data.append(categ_data)
            parent_categ=categ_data
            if categ_data and categ_data.parent_id:
                parent_categ=categ_data.parent_id
                data.append(parent_categ)           
                while parent_categ.parent_id:
                    parent_categ=parent_categ.parent_id
                    data.append(parent_categ) 
            data.reverse()     
        return data

    @api.model
    def new_page(self, name, template='website.default_page', ispage=True):        
        template_module, dummy = template.split('.')
        website_id = self._context.get('website_id')

        # completely arbitrary max_length
        page_name = slugify(name, max_length=50)
        page_xmlid = "%s.%s" % (template_module, page_name)

        # find a free xmlid
        inc = 0
        domain_static = [('website_id', '=', False), ('website_id', '=', website_id)]
        while self.env['ir.ui.view'].with_context(active_test=False).sudo().search([('key', '=', page_xmlid), '|'] + domain_static):
            inc += 1
            page_xmlid = "%s.%s" % (template_module, page_name + ("-%s" % inc if inc else ""))
        page_name += (inc and "-%s" % inc or "")

        # new page
        template_record = self.env.ref(template)
        key = '%s.%s' % (template_module, page_name)
        page = template_record.copy({'website_id': website_id, 'key': key})
        page.with_context(lang=None).write({
            'arch': page.arch.replace(template, page_xmlid),
            'name': page_name,
            'page': ispage,
        })
        arch = "<?xml version='1.0'?><t t-name='website."+str(page_name)+"'><t t-call='website.layout'> \
                <div id='wrap' class='oe_structure oe_empty'>"

        arch=arch+'<t t-if="not website.is_breadcum">'

        arch =arch+'<t t-if="not website.bread_cum_image">'\
            '<nav class="is-breadcrumb shop-breadcrumb" role="navigation" aria-label="breadcrumbs">'\
                  '<div class="container">'\
                    '<h1><span>'+str(page_name)+'</span></h1>'\
                    '<ul class="breadcrumb">'\
                        '<li><a href="/page/homepage">Home</a></li>'\
                        '<li class="active"><span>'+str(page_name)+'</span></li>'\
                    '</ul>'\
                  '</div>'\
            '</nav>'\
            '</t>'
        arch=arch+'<t t-if="website.bread_cum_image">'\
            '<t t-set="bread_cum" t-value="website.image_url(website,'+repr('bread_cum_image')+')"/>'\
            '<nav class="is-breadcrumb shop-breadcrumb" role="navigation" aria-label="breadcrumbs" t-attf-style="background-image:url(#{bread_cum}#)">'\
                '<div class="container">'\
                    '<h1><span>'+str(page_name)+'</span></h1>'\
                    '<ul class="breadcrumb">'\
                        '<li><a href="/page/homepage">Home</a></li>'\
                        '<li class="active"><span>'+str(page_name)+'</span></li>'\
                    '</ul>'\
                  '</div>'\
            '</nav>'\
        '</t>'
        arch =arch+'</t>'
        arch = arch+'</div><div class="oe_structure"/></t></t>'
        page.with_context(lang=None).write({
            'arch': arch,
        })
        return page_xmlid

class WebsiteConfigSettings(models.TransientModel):

    """Settings for the Breadcrumb."""

    _inherit = 'website.config.settings'

    bread_cum_image = fields.Binary(
        related='website_id.bread_cum_image',
        string='Breadcrumb Image',
    )
    is_breadcum = fields.Boolean(string="Do you want to disable Breadcrumb?", related='website_id.is_breadcum',)

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    hover_image = fields.Binary("Hover Image")

