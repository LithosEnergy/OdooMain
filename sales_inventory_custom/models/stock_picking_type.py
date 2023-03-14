# -*- coding: utf-8 -*-
from odoo import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    type_approval_id = fields.Many2one(
        "stock.transfer.approval.temp", string="Approval Template"
    )
