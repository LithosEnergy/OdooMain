from odoo import models, api, fields, _
import requests
import json
from ..unit.bill_importer import Billcom_BillImport
from ..unit.bill_exporter import Billcom_BillExport


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    bill_id = fields.Char('Bill Id')
    bill_sync = fields.Boolean(string='Bill Sync', readonly=True, default=False)

class AccountMove(models.Model):
    _inherit = "account.move"

    bill_id = fields.Char('Bill Id')
    bill_sync = fields.Boolean(string='Bill Sync', readonly=True, default=False)
    token = fields.Char('token')
    challengeid = fields.Char('challengeId')
    session_id = fields.Char('challengeId')

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def importer(self, backend):
        importer = Billcom_BillImport(backend)
        arguments = []

        count = 0
        data = True
        bill_record_list = []
        while(data): 
            result = importer.import_bill(backend,arguments,count)
            if result.json()['response_message'] == "Success" and (len(result.json()['response_data']) !=0):
                for record in result.json()['response_data']:
                    # if record['paymentStatus'] == "1" or record['paymentStatus'] == "4":
                    if (record['paymentStatus'] == "0") and (record['isActive'] == "1"):                      
                        bill_record_list.append(record)
            else:
                data = False                
            count += 100


        if bill_record_list:
            for bill_record in bill_record_list:
                self.single_importer(backend, bill_record)

    def single_importer(self,backend,bill_record):
        importer = Billcom_BillImport(backend)
        if 'id' in bill_record:
            bill_id = bill_record['id']
        else:
            bill_id = bill_record #when bill_record is integer
            arguments = [bill_id]
            result = importer.import_bill(backend,arguments)
            bill_record = result.json()['response_data']

        mapper = self.env['account.move'].search([('bill_id','=',bill_id)],limit=1) 

        if mapper:            
            if bill_record['paymentStatus'] == "0":#payment creation
                if mapper.state == "posted" and mapper.invoice_payment_state != 'paid':
                    vals = {
                            'payment_type': 'outbound',
                            'amount': mapper.amount_total,
                            'currency_id': self.env.company.currency_id.id,
                            'journal_id': self.env['account.journal'].search([('name','=','Bank')], limit=1).id,
                            'company_id': self.env.ref('base.main_company').id,
                            'payment_date': mapper.date,
                            'partner_id': mapper.partner_id.id,
                            'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
                            # 'destination_journal_id': dest_journal_id.id,
                            'partner_type': 'supplier',
                            'invoice_ids': [(6, 0, mapper.ids)],
                            'communication':mapper.name
                        }

                    payment = self.env['account.payment'].create(vals)
                    payment.post()
                    mapper.bill_id = bill_id
                    mapper.bill_sync = True

                # if mapper.invoice_payment_state == 'paid':
                #     mapper.export(backend)                


    def export(self, backend):
        """ export bills or update backend mapper """
        if len(self.ids)>1:
            for obj in self:
                obj.export(backend)
            return

        for line in self.invoice_line_ids:#if account not added in bill line 
            if not line.account_id:
                return

        mapper = self.env['account.move'].search([('bill_sync', '=',True), ('id', '=', self.id)], limit=1)
        
        arguments = [mapper.bill_id or None, self]

        export = Billcom_BillExport(backend)
        res = export.export_bill(backend, arguments)
        bill_record = res.json()['response_data']
        print("export bill",bill_record)
        if bill_record:
            self.bill_id = bill_record['id']
            self.bill_sync = True
            mfa_result = export.MFAChallenge(backend, arguments)
            if mfa_result.json()['response_message'] == 'Success':
                self.challengeid = mfa_result.json()['response_data']['challengeId']


    def custom_action_invoice_register_payment(self):
        """ export bills or update backend mapper """
        if self:
            backend = self.env['billdotcom.configure'].search([],limit=1)
            for record in self:
                record.export(backend)

    def pay_amount(self):
        if self:
            backend = self.env['billdotcom.configure'].search([],limit=1)
            """ export bills or update backend mapper """
            if len(self.ids)>1:
                for obj in self:
                    obj.export(backend)
                return

            for line in self.invoice_line_ids:#if account not added in bill line 
                if not line.account_id:
                    return

            mapper = self.env['account.move'].search([('bill_sync', '=',True), ('id', '=', self.id)], limit=1)
            arguments = [mapper.bill_id or None, self]
            export = Billcom_BillExport(backend)
            mfa_auth_result = export.MFAAuthenticate(backend, arguments)
            print('mfa_auth_result',mfa_auth_result.json())
            if mfa_auth_result.json()['response_message'] == 'Success':
                bill_paid = export.pay_bill(backend, arguments)



