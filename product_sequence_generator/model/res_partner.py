from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    manufacturer = fields.Boolean("Manufacturer", default=False, copy=False)
