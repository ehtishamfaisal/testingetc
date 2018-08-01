# -*- coding: utf-8 -*-

import datetime
import json
import werkzeug

from odoo import tools
from odoo.addons.website.models.website import slug, unslug
from odoo.exceptions import UserError
from odoo.osv.orm import browse_record
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from odoo.tools import html2plaintext
from odoo import http
from odoo.http import request
from openerp.addons.website_blog.controllers.main import WebsiteBlog

class WebsiteBlog(WebsiteBlog):

	@http.route(['/blog/get_blog_content'], type='http', auth='public', website=True)
	def get_blog_content_data(self, **post):
		value={}
		if post.get('blog_config_id')!='false':
			collection_data=request.env['blog.configure'].browse(int(post.get('blog_config_id')))
			value.update({'blog_slider':collection_data})
		return request.render("theme_watch.blog_slider_content", value)

