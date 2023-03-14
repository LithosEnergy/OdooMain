# -*- coding: utf-8 -*-

from odoo import models, fields


class StockApprovalLine(models.Model):
    _name = "stock.approval.line"
    _description = "Stock Approvals Line"

    name = fields.Char(string="role")
    approved_by = fields.Many2one("res.users", string="Approved By")
    status = fields.Selection(
        [
            ("not_yet", "Not Yet"),
            ("approved", "Approved"),
            ("reject", "Reject"),
            ("submitted", "Submitted"),
        ],
        string="Status",
        default="not_yet",
    )

    approval_date = fields.Date(string="Approval Date")
    approval_stage_id = fields.Many2one(
        "stock.transfer.approval.temp", string="Approval Stage"
    )
    req_user_ids = fields.Many2many("res.users", string="Requested Users")
    picking_approve_id = fields.Many2one("stock.picking", string="picking")
    is_valid_user = fields.Boolean(string="Is Valid User")
