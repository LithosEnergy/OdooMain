from odoo import models,fields,api


class MRPProduction(models.Model):
    _inherit ="mrp.production"

    project_code = fields.Char(string="Project Code")




