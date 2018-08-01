
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    wk_type = fields.Selection([('dt','Dining Tables'),('dts','Dining Tables Sets'),('kt','Kitchen Tables'),('kt','Kitchen Tables'),('ot','Occasional Tables'),('b','Benches'),('kts','Kitchen Table Sets')], default='kt', string="Website Type(Product)")
#Dimensions
    height = fields.Char('Height(cm)')
    length = fields.Char('Length(cm)')
    widtht = fields.Char('Width(cm)')
    additional_dimensions = fields.Char('Additional Dimensions(cm)')
    packing_dimensions = fields.Char('Packing Dimensions')
    sizes = fields.Char("Sizes")

#Additional Information
    weight = fields.Float('Weight(Kg)')
    material = fields.Char('Material')
    finish = fields.Char('Finish')
    assembly = fields.Char('Assembly')
    caring_instructions = fields.Char('Caring Instructions')
    special_features = fields.Char('Special Features')
