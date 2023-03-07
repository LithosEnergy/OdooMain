from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    production_state = fields.Many2one(
        "production.state",
        string="Production State",
        readonly=True,
        tracking=True,
        copy=False,
    )
    manufacturer = fields.Many2one(
        "res.partner",
        string="Manufacturer",
        domain="[('manufacturer', '=', True)]",
        copy=False,
    )
    manufacturer_part_number = fields.Char(
        string="Manufacturer Part Number", copy=False
    )
