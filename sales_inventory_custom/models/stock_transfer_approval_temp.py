# -*- coding: utf-8 -*-

from odoo import models, fields


class StockTransferApprovalTemp(models.Model):
    _name = "stock.transfer.approval.temp"
    _description = "Stock Approvals Templates"

    name = fields.Char(string="Name")
    approval_item_ids = fields.One2many(
        "stock.transfer.approval.temp.items", "approval_id", string="Approvals"
    )
