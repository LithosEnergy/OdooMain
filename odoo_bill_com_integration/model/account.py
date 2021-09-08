from odoo import models, api, fields, _
import requests
import json
from ..unit.account_exporter import Billcom_AccountExport


class Account(models.Model):
    _inherit = 'account.account'


    bill_id = fields.Char('Bill Id')
    bill_sync = fields.Boolean(string='Bill Sync', readonly=True, default=False)
    bill_account_type = fields.Integer('Bill Account Type')


    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def export(self, backend):
        """ export chart of account details and update mapper """
        if len(self.ids)>1:
            for obj in self:
                obj.export(backend)
            return
        if not self.bill_account_type:
            return
        
        mapper = self.env['account.account'].search([('bill_sync', '=',True), ('id', '=', self.id)], limit=1)
        
        arguments = [mapper.bill_id or None, self]

        export = Billcom_AccountExport(backend)
        res = export.export_account(backend, arguments)
        account_record = res.json()['response_data']
        print("export account",account_record)
        if account_record:
            self.bill_id = account_record['id']
            self.bill_sync = True




