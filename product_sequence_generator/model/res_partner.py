from odoo import models, fields, api, _


class Res_Partner(models.Model):
    _inherit = 'res.partner'

    manufacturer = fields.Boolean("Manufacturer")

