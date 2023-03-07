from odoo import models, fields


class InheritMrpEcoStage(models.Model):
    _inherit = "mrp.eco.stage"

    check_production_state = fields.Boolean(string="Check Production State")
