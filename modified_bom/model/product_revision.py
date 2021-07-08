from odoo import models, fields, api, _

class Product_Revisions(models.Model):
    _inherit = 'product.revisions'

    bom_version = fields.Integer(string="BOM Version")
