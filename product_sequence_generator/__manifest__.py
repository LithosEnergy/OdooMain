# -*- coding: utf-8 -*-
{
    'name': "Product Sequence Generator",

    'summary': """
     Product sequence Generat in Internal Refrence
       """,

    'description': """
        Product sequence Generat in Internal Refrence
    """,
     'author': "Techspawn Solutions",
    'website': "http://www.techspawn.com",
    'category': 'Manufacturing',
    'version': '13.0.0',
    'depends': ['base','mrp_plm', 'purchase_stock'],
    'data': [
        'wizard/generate_new_product.xml',
    ],
    'demo': [
        'demo/product_sequence_data.xml',
    ],
}