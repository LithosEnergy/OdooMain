from odoo import models, fields


class MRPProduction(models.Model):
    _inherit = "mrp.production"

    project_code = fields.Char(string="Project Code")
