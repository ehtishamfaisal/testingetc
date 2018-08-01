
from odoo import models, fields, api

class multitab_configure(models.Model):
    _name = 'multitab.configure'

    name= fields.Char("Group Name",translate=True)
    product_ids=fields.Many2many("product.template",string="Products")
    active=fields.Boolean("Active")

class collection_configure(models.Model):

	_name = 'collection.configure'

	name=fields.Char("Title")
	tab_collection_ids=fields.Many2many('multitab.configure',string="Select Collection",translate=True)
	active=fields.Boolean("Active")

