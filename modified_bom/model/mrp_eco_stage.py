from odoo import models, fields, api, _

class Inherit_MrpEcoStage(models.Model):
    _inherit = 'mrp.eco.stage'

    check_production_state = fields.Boolean(string="Check Production State")
