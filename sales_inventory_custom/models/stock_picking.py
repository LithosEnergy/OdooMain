# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import api, models, fields, _
from datetime import date


class StockPicking(models.Model):
    _inherit = "stock.picking"

    approval_temp_id = fields.Many2one(
        "stock.transfer.approval.temp", string="Approval Template"
    )
    approval_line_ids = fields.One2many(
        "stock.approval.line", "picking_approve_id", string="approvals"
    )
    new_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("need_approval", "Needs Approval"),
            ("waiting", "Waiting Another Operation"),
            ("confirmed", "Waiting"),
            ("assigned", "Ready"),
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        string="New State",
        compute="_compute_new_state",
        copy=False,
    )
    submit_approval = fields.Boolean(string="Submit Approval", copy=False)
    state = fields.Selection(
        selection_add=[("need_approval", "Needs Approval")]
    )
    fully_approved = fields.Boolean(
        compute="_compute_fully_approved", copy=False
    )
    valid_for_approval = fields.Boolean(
        compute="_compute_valid_for_approval", copy=False
    )
    valid_for_reject = fields.Boolean(
        compute="_compute_valid_for_reject", copy=False
    )
    approval_history_ids = fields.One2many(
        "stock.approval.history",
        "picking_history_id",
        string="Approval History",
    )

    @api.depends("approval_line_ids", "submit_approval", "new_state")
    def _compute_valid_for_approval(self):
        valid_for_approval = False
        for obj in self:
            if obj.submit_approval and not obj.fully_approved:
                find_line_not_approved = obj.approval_line_ids.filtered(
                    lambda x: self.env.uid in x.req_user_ids.ids
                    and x.status in ("submitted", "reject")
                )
                if find_line_not_approved:
                    valid_for_approval = True
            obj.valid_for_approval = valid_for_approval

    @api.depends("approval_line_ids", "submit_approval", "new_state")
    def _compute_valid_for_reject(self):
        valid_for_reject = False
        for obj in self:
            if obj.submit_approval and not obj.fully_approved:
                find_line_not_reject = obj.approval_line_ids.filtered(
                    lambda x: self.env.uid in x.req_user_ids.ids
                    and x.status in ("submitted", "approved")
                )
                if find_line_not_reject:
                    valid_for_reject = True
            obj.valid_for_reject = valid_for_reject

    def action_reject(self):
        reject_line_history = []
        for obj in self:
            find_line_not_reject = obj.approval_line_ids.filtered(
                lambda x: self.env.uid in x.req_user_ids.ids
                and x.status in ("submitted", "approved")
            )
            if find_line_not_reject:
                for line in find_line_not_reject:
                    line.status = "reject"
                    line.approved_by = self.env.user.id
                    line.approval_date = date.today()
                    vals = {
                        "name": line.name,
                        "status": "reject",
                        "approval_stage_id":
                            self.picking_type_id.type_approval_id.id,
                        "picking_approve_id": self.id,
                        "approved_by": self.env.user.id,
                        "approval_date": date.today(),
                    }
                    reject_line_history.append((0, 0, vals))
            obj.approval_history_ids = reject_line_history
        return True

    def action_approve(self):
        approve_line_history = []
        for obj in self:
            find_line_not_approved = obj.approval_line_ids.filtered(
                lambda x: self.env.uid in x.req_user_ids.ids
                and x.status in ("submitted", "reject")
            )
            if find_line_not_approved:
                for line in find_line_not_approved:
                    line.status = "approved"
                    line.approved_by = self.env.user.id
                    line.approval_date = date.today()
                    vals = {
                        "name": line.name,
                        "status": "approved",
                        "approval_stage_id":
                            self.picking_type_id.type_approval_id.id,
                        "picking_approve_id": self.id,
                        "approved_by": self.env.user.id,
                        "approval_date": date.today(),
                    }
                    approve_line_history.append((0, 0, vals))
            obj.approval_history_ids = approve_line_history
        return True

    @api.depends("approval_line_ids")
    def _compute_fully_approved(self):
        fully_approved = False
        for obj in self:
            if obj.approval_line_ids:
                fully_approved = all(
                    line.status == "approved" for line in obj.approval_line_ids
                )
        obj.fully_approved = fully_approved

    @api.onchange("picking_type_id")
    def onchange_picking_type_approval(self):
        for obj in self:
            approval_list = []
            if (
                not obj.picking_type_id
                or not obj.picking_type_id.type_approval_id
            ):
                obj.approval_temp_id = False
                return
            if obj.picking_type_id and obj.picking_type_id.type_approval_id:
                obj.approval_temp_id = obj.picking_type_id.type_approval_id.id
                for (
                    item
                ) in obj.picking_type_id.type_approval_id.approval_item_ids:
                    vals = {
                        "name": item.name,
                        "status": "not_yet",
                        "approval_stage_id":
                            obj.picking_type_id.type_approval_id.id,
                        "picking_approve_id": obj.id,
                    }
                    if item.user_ids:
                        vals.update(
                            {"req_user_ids": [(6, 0, item.user_ids.ids)]}
                        )
                    approval_list.append((0, 0, vals))
                obj.approval_line_ids = approval_list

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        res.onchange_picking_type_approval()
        return res

    @api.onchange("approval_temp_id")
    def onchange_approval_temp(self):
        for obj in self:
            approval_list = []
            obj.approval_line_ids = [(5, 0, 0)]
            if obj.approval_temp_id:
                for item in obj.approval_temp_id.approval_item_ids:
                    vals = {
                        "name": item.name,
                        "status": "not_yet",
                        "approval_stage_id": obj.approval_temp_id.id,
                        "picking_approve_id": obj.id,
                    }
                    if item.user_ids:
                        vals.update(
                            {"req_user_ids": [(6, 0, item.user_ids.ids)]}
                        )
                    approval_list.append((0, 0, vals))
            else:
                obj.approval_line_ids = [(5, 0, 0)]
            obj.approval_line_ids = approval_list

    @api.depends("state")
    def _compute_new_state(self):
        for obj in self:
            new_state = ""
            if obj.state and obj.submit_approval and not obj.fully_approved:
                new_state = "need_approval"
            else:
                new_state = obj.state
            obj.new_state = new_state

    def button_validate(self):
        if self.approval_line_ids:
            not_approved = self.approval_line_ids.filtered(
                lambda x: x.status != "approved"
            )
            if not_approved:
                raise UserError(
                    _(
                        "This stock move can not be performed "
                        " until all approvals have been performed"
                    )
                )
        return super(StockPicking, self).button_validate()

    def button_submit_approval(self):
        IrConfigSudo = self.env["ir.config_parameter"].sudo()
        base_url = IrConfigSudo.get_param("web.base.url") or ""
        email_values = {}
        template_id = self.env["ir.model.data"]._xmlid_to_res_id(
            "sales_inventory_custom.stock_approval_request_mail_template",
            raise_if_not_found=False,
        )
        template = self.env["mail.template"].browse(template_id)
        url_id = "%s/web#id=%s&model=stock.picking" % (base_url, str(self.id))
        if self.approval_line_ids:
            for line in self.approval_line_ids:
                line.status = "submitted"
                for user in line.req_user_ids:
                    if user.partner_id and user.partner_id.email and template:
                        email_values = {
                            "email_to": user.partner_id.email,
                            "url_id": url_id,
                        }
                        template[0].with_context(email_values).send_mail(
                            self.id, force_send=True
                        )
            self.submit_approval = True
        return True
