# -*- coding: utf-8 -*-
{
    'name': "Blanket Sales Order App",
    'author': "Edge Technologies",
    'version' : '13.0.1.0',
    'live_test_url':'https://youtu.be/B6SZKtvT_8o',
    "images":["static/description/main_screenshot.png"],
    'summary':'Blanket Sale Order Manage Blanket Orders Sale Blanket Orders for Sales Process Sales Agreement Sale Agreement Sales Blanket Orders Agreement Orders Seller Agreement Customer Agreement Order for Customer Agreement Orders for Sellers Blanket Order Mass Order',
    'description': """
      In This Application you Allows to Create Blanket Sale Order. In that Sales Team Create and Manage Blanket Sales Orders and Allow them to Create Sales Orders.
    """,
    'depends': ['base','sale_management','account'],
    "license" : "OPL-1",
    'data': [
    
    'security/ir.model.access.csv',
    'wizard/blanket_sale_wizard.xml',
    'data/sequence.xml',
    'views/sale_view.xml',

    
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price':18,
    'currency': "EUR",
    'category' : 'Sales'
}
