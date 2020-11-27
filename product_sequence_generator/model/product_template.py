from odoo import models, fields, api, _


class Product_Template(models.Model):
    _inherit = 'product.template'

    production_state = fields.Many2one('production.state',string='Production State',readonly=True, track_visibility='onchange')
    manufacturer = fields.Many2one('res.partner',string="Manufacturer",domain="[('manufacturer', '=', True)]")
    manufacturer_part_number = fields.Char(string="Manufacturer Part Number")

