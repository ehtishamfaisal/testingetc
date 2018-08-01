
from odoo import api, fields, models
from odoo.models import Model
from urlparse import urljoin
from odoo.addons.website.models.website import slug

class ProductWishlist(Model):
    _name = "product.wishlist"

    user_id = fields.Many2one("res.users",string="User Id")
    product_id = fields.Many2one("product.product",string="Product")
    comment=fields.Text("Comment",translate=True)

    
class website(Model):
    _inherit='website'

    @api.model
    def check_product_in_wishlist(self,product_id=None):
        if product_id:
            check=self.env['product.wishlist'].search([('user_id','=',self._uid),('product_id','=',product_id)])
            if check:
                return True
        return False
