from odoo import models, fields


class ProductRevisions(models.Model):
    _inherit = "product.revisions"

    bom_version = fields.Integer(string="BOM Version")
