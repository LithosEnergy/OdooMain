import logging
from odoo import models, api, fields, _
import requests
import json
from ..unit.backend_adapter import Billcom_ImportExport
_logger = logging.getLogger(__name__)


class Billcom_AccountExport(Billcom_ImportExport):

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def export_account(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key
        if not arguments[0]:
            login_end_point = str(url) + 'Crud/Create/ChartOfAccount.json'           
            dict_val = {
                    "obj": {
                        "entity":"ChartOfAccount",
                        "isActive":"1",
                        "name":str(arguments[1].name),
                        "accountNumber" : str(arguments[1].code),
                        "accountType" : str(arguments[1].bill_account_type),
                        }
                    }
                    
        else:
            login_end_point = str(url) + 'Crud/Update/ChartOfAccount.json'           
            dict_val = {
                    "obj": {
                        "entity":"ChartOfAccount",
                        "id" :str(arguments[1].bill_id),
                        "isActive":"1",
                        "name":str(arguments[1].name),
                        "accountNumber" : str(arguments[1].code),
                        "accountType" : str(arguments[1].bill_account_type),
                        }
                    }

        params_str = "devKey=" + str(devkey) + "&sessionId=" + str(session_id) + "&data=" + str(self.mydict(dict_val))
        
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result