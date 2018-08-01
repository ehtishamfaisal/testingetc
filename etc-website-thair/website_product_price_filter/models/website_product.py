# -*- coding: utf-8 -*-

from odoo import api, fields , models
from __builtin__ import str

class WkProductPrice(models.Model):
	_name = "wk.product.price"
	_order = 'sequence'
	
	name = fields.Char(string="Price Label",required=True, translate=True)
	min_price = fields.Float(string="Min Price",required=True)
	max_price = fields.Float(string="Max Price",required=True)
	sequence = fields.Integer(string = "Sequence")

	@api.model
	def wk_activate_website_view(self):
		products_description = self.env.ref('website_sale.products_description')
		products_attributes = self.env.ref('website_sale.products_attributes')
		products_description.write(dict(active=1))
		products_attributes.write(dict(active=1))
		return True


class LegStyle(models.Model):
	_name = "leg.style"
	_order = 'sequence'
	
	name = fields.Char(string="Name",required=True, translate=True)
	sequence = fields.Integer(string = "Sequence")

class TableStyle(models.Model):
	_name = "table.style"
	_order = 'sequence'
	
	name = fields.Char(string="Name",required=True, translate=True)
	sequence = fields.Integer(string = "Sequence")

class TableFinish(models.Model):
	_name = "table.finish"
	_order = 'sequence'
	
	name = fields.Char(string="Name",required=True, translate=True)
	sequence = fields.Integer(string = "Sequence")

class ProductTemplate(models.Model):
	_inherit = 'product.template'
	
	leg_style_ids = fields.Many2many('leg.style', string="Leg Style")
	table_style_ids = fields.Many2many('table.style', string="Table Style")
	sku_code = fields.Char("SKU (Code)")
	
class website(models.Model):
	_inherit = 'website'

	def get_wk_price(self,price_set):
		return self.env['wk.product.price'].sudo().browse(list(set(price_set)))

	def get_filter_brand(self,wk_price):
		filter_brand=''
		for wk_price in wk_price:
			filter_brand+='%s,'%(wk_price.id)
		return filter_brand
		return ','.join(map(str,wk_price.ids))


