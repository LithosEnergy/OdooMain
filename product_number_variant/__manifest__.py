# -*- coding: utf-8 -*-
{
    'name': "Product Number Variant",

    'summary': """
     Product Number Variant Generate in Internal Refrence
       """,

    'description': """
        Product Number Variant Generate in Internal Refrence
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'Manufacturing',
    'version': '13.0.0',
    'depends': ['base','mrp_plm', 'purchase_stock','product_sequence_generator'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_variant.xml',
    ],
    'demo': [
    ],
}
