from odoo import models, fields


class inherit_Production_State(models.Model):
    _inherit = "production.state"

    sequence = fields.Integer("Sequence")
