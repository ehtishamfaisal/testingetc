from odoo import api, fields, models
from odoo.models import Model
from urlparse import urljoin
from odoo.addons.website.models.website import slug

class mega_menu_content(Model):
    _name='megamenu.content'
    
    name=fields.Char("Content Name",translate=True)
    active=fields.Boolean("Active",default=True)
    is_header=fields.Boolean("Header")
    is_footer=fields.Boolean("Footer")
    main_content_type=fields.Selection([('product_grid','Product Grid'),('product_list','Product Listing'),
                                        ('category_grid','Category Grid'),('category_list','Category Listing'),
                                        ('content','Content')],translate=True)
    no_of_columns=fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6')],
                                   string="Number of Columns",translate=True)
    product_ids=fields.Many2many("product.template",string="Products", domain=[('website_published','=',True)])
    product_lable_color=fields.Char("Product Label Color")
    header_content=fields.Html("Header Content",translate=True)
    footer_content=fields.Html("Footer Content",translate=True)
    category_ids=fields.Many2many("product.public.category",string="Category", domain=['|',('parent_id','=',False),('parent_id.parent_id','=',False)])
    category_lable_color=fields.Char("Category Label Color")
    menu_content=fields.Html("Content",translate=True)
    
    
class website_menu(Model):
    _inherit="website.menu"
    
    is_mega_menu=fields.Boolean("Mega Menu")
    content_id=fields.Many2one("megamenu.content","Content")
    parent_id=fields.Many2one('website.menu', 'Parent Menu', select=True, ondelete="cascade",domain=[('is_mega_menu','=',False)])
    

    
    
