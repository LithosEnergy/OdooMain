from odoo import models, api, fields, _
import requests
import json
from ..unit.vendor_exporter import Billcom_VendorExport

class Partner(models.Model):
    _inherit = 'res.partner'

    bill_id = fields.Char('Bill Id')
    bill_sync = fields.Boolean(string='Bill Sync', readonly=True, default=False)

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def export(self, backend):
        """ export vendor details, save username and create or update backend mapper """
        if len(self.ids)>1:
            for obj in self:
                obj.export(backend)
            return
        if not self.supplier_rank > 0:
            return
        mapper = self.env['res.partner'].search([('bill_sync', '=',True), ('id', '=', self.id)], limit=1)
        
        arguments = [mapper.bill_id or None, self]

        export = Billcom_VendorExport(backend)
        res = export.export_vendor(backend, arguments)
        vendor_record = res.json()['response_data']
        print("export vendor",vendor_record)
        if vendor_record:
            self.bill_id = vendor_record['id']
            self.bill_sync = True


