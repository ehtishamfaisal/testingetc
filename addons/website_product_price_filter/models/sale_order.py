# -*- coding: utf-8 -*-

from odoo import api, fields , models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    finish_id = fields.Many2one('table.finish', 'Finish')
