from odoo import models, fields


class InheritMrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    production_state_id = fields.Many2one(
        "production.state",
        related="product_id.production_state",
        string="Production State")
