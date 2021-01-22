from odoo import models, fields, api, _
from odoo.exceptions import UserError

class inherit_Production_State(models.Model):
    _inherit = 'production.state'

    sequence = fields.Integer("Sequence")

   