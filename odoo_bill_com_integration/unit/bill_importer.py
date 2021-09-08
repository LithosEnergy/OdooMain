import logging
from odoo import models, api, fields, _
import requests
import json
from datetime import datetime
from odoo.exceptions import UserError, RedirectWarning, ValidationError, Warning
from ..unit.backend_adapter import Billcom_ImportExport
_logger = logging.getLogger(__name__)


class Billcom_BillImport(Billcom_ImportExport):

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def import_bill(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key
        if not arguments:
            login_end_point = str(url) + 'List/Bill.json'           
            dict_val={
                        "nested" : True,
                        "start" : count,#page number
                        "max" : 100,#records per page
                    }
        else:
            login_end_point = str(url) + 'Crud/Read/Bill.json'           
            dict_val={
                        "id" : arguments[0]
                    }

        params_str = "devKey=" + str(devkey) + "&sessionId=" + str(session_id) + "&data=" + str(self.mydict(dict_val))
        
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result
