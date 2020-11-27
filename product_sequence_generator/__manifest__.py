# -*- coding: utf-8 -*-
{
    'name': "Product Sequence Generator",

    'summary': """
     Product sequence Generat in Internal Refrence
       """,

    'description': """
        Product sequence Generat in Internal Refrence
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'Manufacturing',
    'version': '13.0.1',
    'depends': ['base','mrp_plm', 'purchase_stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/generate_new_product.xml',
        'views/production_state.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
    ],
    'demo': [
        'demo/product_sequence_data.xml',
    ],
}