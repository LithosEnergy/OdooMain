# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2016-Present Techspawn Solutions Pvt. Ltd.
# (<https://techspawn.com/>)
#
##########################################################################

{
    'name': 'Odoo Bill.com Integration',
    'version': '13.0',
    'category': 'custom',
    'sequence': 1,
    'license': 'OPL-1',
    'price': 95.00,
    'currency': 'USD',
    'author': 'Techspawn Solutions Pvt. Ltd.',
    'website': 'http://www.techspawn.com',
    'description': """

Odoo Bill.com Connect
=========================

This Module will Connect Odoo with Bill.com and synchronise Data.
------------------------------------------------------------------------------


Some of the feature of the module:
--------------------------------------------

  1. Export the Bills to bill.com.
  2. Update status "ready to pay" of bills of bill.com
  3. Get back paid status in odoo and update paid status of bill in odoo

----------------------------------------------------------------------------------------------------------
    """,
    'demo_xml': [],
    'update_xml': [],
    'depends': ['base',
                'sh_message',
                'stock',
                'sale_management',
                'purchase',
                'account',
                ],
    'data': [
                'security/bridge_security.xml',
                'security/ir.model.access.csv',
                'views/bridge_view.xml',
                'views/vendor.xml',
                'views/account.xml',
                'views/bill.xml',
                'views/cron.xml',
             ],
    'js': [],
    'images': ['images/Bill_Com.gif'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
