# -*- coding: utf-8 -*-

from odoo import models, fields


class StockTransferApprovalTempItems(models.Model):
    _name = "stock.transfer.approval.temp.items"
    _description = "Stock Approvals Templates Items"
    _order = "sequence asc"

    name = fields.Char("Role", required=True)
    sequence = fields.Integer("Sequence")
    approval_type = fields.Selection(
        [
            ("optional", "Approves, but the approval is optional"),
            ("mandatory", "Is required to approve"),
            ("comment", "Comments only"),
        ],
        "Approval Type",
        default="mandatory",
        required=True,
    )
    user_ids = fields.Many2many("res.users", string="Users", required=True)
    approval_id = fields.Many2one(
        "stock.transfer.approval.temp", string="Approval"
    )
