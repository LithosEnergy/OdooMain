import logging
from odoo import models, api, fields, _
import requests
import json
from datetime import date
from ..unit.backend_adapter import Billcom_ImportExport
_logger = logging.getLogger(__name__)


class Billcom_BillExport(Billcom_ImportExport):

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def export_bill(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        arguments[1].session_id = session_id
        print("session_id",session_id)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key
        if not arguments[1].partner_id.bill_sync:
            arguments[1].partner_id.export(backend)
        
        dict_val = {
                    "obj": {
                        "entity" : "Bill",
                        "isActive" : "1",
                        # "description":"Ready For Payment!!",
                        "vendorId" : str(arguments[1].partner_id.bill_id),
                        "dueDate" : str(arguments[1].invoice_date_due),
                        "invoiceDate" : str(arguments[1].invoice_date),
                        "invoiceNumber":str(arguments[1].name),
                        "billLineItems" : []
                    }
                }  

        # if arguments[1].invoice_payment_state == "paid":
        #     dict_val['obj'].update({"description":""})
        # else:
        #     dict_val['obj'].update({"description":"Ready For Payment!!"})       
        
        for line in arguments[1].invoice_line_ids:
            if not line.account_id.bill_sync:
                line.account_id.export(backend)

            vals = {
                "entity" : "BillLineItem",
                "amount" : line.price_subtotal,
                "chartOfAccountId" : str(line.account_id.bill_id),
                "quantity" : line.quantity,
                "unitPrice" : line.price_unit,
                "lineType" : "1",
                "description":line.name or "",             
            }
            if dict_val['obj']['billLineItems']:
                for record in dict_val['obj']['billLineItems']:
                    if record['chartOfAccountId'] == vals['chartOfAccountId']:
                        record['amount'] = record['amount']+vals['amount']
                        record['quantity'] = record['quantity']+vals['quantity']
                        record['unitPrice'] = record['unitPrice']+vals['unitPrice']
                        break

                    else:
                        dict_val['obj']['billLineItems'].append(vals)
                        break
            else:
                dict_val['obj']['billLineItems'].append(vals)


        if not arguments[0]:
            login_end_point = str(url) + 'Crud/Create/Bill.json'       
                    
        else:
            login_end_point = str(url) + 'Crud/Update/Bill.json' 
            dict_val['obj']['id'] = str(arguments[1].bill_id)        

        params_str = "devKey=" + str(devkey) + "&sessionId=" + str(session_id) + "&data=" + str(self.mydict(dict_val))
        
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result


    def pay_bill(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key
        if not arguments[1].partner_id.bill_sync:
            arguments[1].partner_id.export(backend)

        dict_val = {"vendorId" : str(arguments[1].partner_id.bill_id),"billPays" : [ {"billId" : str(arguments[1].bill_id), "amount" : arguments[1].amount_total }],"billCredits":[]}
        login_end_point = str(url) + 'PayBills.json' 
        params_str = "devKey=" + str(devkey) + "&sessionId=" + arguments[1].session_id + "&data=" + str(self.mydict(dict_val))
        
        result = requests.post(login_end_point, data=params_str, headers=headers)
        print("pay_bill",result.json())
        return result


    def MFAChallenge(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key

        login_end_point = str(url) + 'MFAChallenge.json'
        dict_val = { "useBackup" : False}
        params_str = "devKey=" + str(devkey) + "&sessionId=" + arguments[1].session_id + "&data=" + str(self.mydict(dict_val))
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result

    def MFAAuthenticate(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key

        login_end_point = str(url) + 'MFAAuthenticate.json'
        dict_val = {"challengeId" : arguments[1].challengeid,"token" : arguments[1].token,"deviceId" : "916E333F-1BBC-4471-946D-8059DB9488B6","machineName" : "Pravin's iPhone","rememberMe" : True        }
        params_str = "devKey=" + str(devkey) + "&sessionId=" + arguments[1].session_id + "&data=" + str(self.mydict(dict_val))
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result





