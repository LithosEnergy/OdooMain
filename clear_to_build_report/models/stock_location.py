# -*- coding: utf-8 -*-

from odoo import models, fields, api

class QualityLocation(models.Model):
	_inherit = "stock.location"

	x_preinspection = fields.Boolean('Pre Inspection Location')