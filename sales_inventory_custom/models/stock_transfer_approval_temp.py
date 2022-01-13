# -*- coding: utf-8 -*-

from datetime import date, datetime
from odoo import api, models, fields

class StockTransferApprovalTemp(models.Model):
    _name = 'stock.transfer.approval.temp'
    _description = 'Stock Approvals Templates'

    name = fields.Char(string="Name")
    approval_item_ids = fields.One2many('stock.transfer.approval.temp.items','approval_id',string="Approvals")

class StockTransferApprovalTempItems(models.Model):
    _name = 'stock.transfer.approval.temp.items'
    _description = 'Stock Approvals Templates Items'
    _order = 'sequence asc'

    name = fields.Char('Role', required=True)
    sequence = fields.Integer('Sequence')
    approval_type = fields.Selection([
        ('optional', 'Approves, but the approval is optional'),
        ('mandatory', 'Is required to approve'),
        ('comment', 'Comments only')], 'Approval Type',
        default='mandatory', required=True)
    user_ids = fields.Many2many('res.users', string='Users', required=True)
    approval_id = fields.Many2one('stock.transfer.approval.temp',string="Approval")    


class StockApprovalLine(models.Model):
    _name = 'stock.approval.line'
    _description = 'Stock Approvals Line'

    name = fields.Char(string="role")
    approved_by = fields.Many2one('res.users', string="Approved By")
    status = fields.Selection([
                        ('not_yet','Not Yet'),
                        ('approved','Approved'),
                        ('reject','Reject'),
                        ('submitted','Submitted')], 
                        string="Status", default="not_yet")
    
    approval_date = fields.Date(string="Approval Date")
    approval_stage_id = fields.Many2one('stock.transfer.approval.temp', string="Approval Stage")
    req_user_ids = fields.Many2many('res.users', string="Requested Users")
    picking_approve_id = fields.Many2one('stock.picking', string="picking")
    is_valid_user = fields.Boolean(string="Is Valid User")


class StockApprovalHistory(models.Model):
    _name = 'stock.approval.history'
    _description = 'Stock Approvals History'
    _order = 'id desc'

    name = fields.Char(string="role")
    approved_by = fields.Many2one('res.users', string="Approved By")
    status = fields.Selection([
                        ('not_yet','Not Yet'),
                        ('approved','Approved'),
                        ('reject','Reject'),
                        ('submitted','Submitted')], 
                        string="Status", default="not_yet")
                            
    approval_date = fields.Date(string="Approval Date")
    approval_stage_id = fields.Many2one('stock.transfer.approval.temp', string="Approval Stage")
    req_user_ids = fields.Many2many('res.users', string="Requested Users")
    picking_approve_id = fields.Many2one('stock.picking', string="picking")
    is_valid_user = fields.Boolean(string="Is Valid User")
    picking_history_id = fields.Many2one('stock.picking', string="Picking History")