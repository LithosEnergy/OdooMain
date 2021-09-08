import logging
from odoo import models, api, fields, _
import requests
import json
from ..unit.backend_adapter import Billcom_ImportExport
_logger = logging.getLogger(__name__)


class Billcom_VendorExport(Billcom_ImportExport):

    class mydict(dict):
        def __str__(self):
            return json.dumps(self)

    def export_vendor(self,backend,arguments,count=None):
        vals = backend.test_connection()
        session_id = vals['result']['response_data']['sessionId']
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = backend.location
        devkey = backend.dev_key
        if not arguments[0]:
            login_end_point = str(url) + 'Crud/Create/Vendor.json'           
            dict_val = {
                    "obj": {
                        "entity":"Vendor",
                        "isActive":"1",
                        "name":str(arguments[1].name),
                        "address1" : str(arguments[1].street) if arguments[1].street else "",
                        "address2" : str(arguments[1].street2) if arguments[1].street2 else "",
                        "address3" : "",
                        "address4" : "",
                        "addressCity" : str(arguments[1].city) if arguments[1].city else "",
                        "addressState" : str(arguments[1].state_id.code) if arguments[1].state_id.code else "",
                        "addressZip" : str(arguments[1].zip) if arguments[1].zip else "",
                        "addressCountry" : str(arguments[1].country_id.code) if arguments[1].country_id.code else "",
                        "email" : str(arguments[1].email) if arguments[1].email else "",
                        "phone":str(arguments[1].phone) if arguments[1].phone else "",
                        }
                    }
                    
        else:
            login_end_point = str(url) + 'Crud/Update/Vendor.json'           
            dict_val = {
                    "obj": {
                        "entity":"Vendor",
                        "id" :str(arguments[1].bill_id),
                        "isActive":"1",
                        "name":str(arguments[1].name),
                        "address1" : str(arguments[1].street) if arguments[1].street else "",
                        "address2" : str(arguments[1].street2) if arguments[1].street2 else "",
                        "address3" : "",
                        "address4" : "",
                        "addressCity" : str(arguments[1].city) if arguments[1].city else "",
                        "addressState" : str(arguments[1].state_id.code) if arguments[1].state_id.code else "",
                        "addressZip" : str(arguments[1].zip) if arguments[1].zip else "",
                        "addressCountry" : str(arguments[1].country_id.code) if arguments[1].country_id.code else "",
                        "email" : str(arguments[1].email) if arguments[1].email else "",
                        "phone":str(arguments[1].phone) if arguments[1].phone else "",
                        }
                    }

        params_str = "devKey=" + str(devkey) + "&sessionId=" + str(session_id) + "&data=" + str(self.mydict(dict_val))
        
        result = requests.post(login_end_point, data=params_str, headers=headers)
        return result