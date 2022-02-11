# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_lot_size = fields.Integer('Lot Size')
