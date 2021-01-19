# -*- coding: utf-8 -*-
{
    'name': "create BOMs via PLM app",

    'summary': """
     Want to create BOMs via PLM app
       """,

    'description': """
        Want to create BOMs via PLM app.
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'Manufacturing',
    'version': '13.0.0',
    'depends': ['base','mrp_plm', 'purchase_stock','product_sequence_generator','product_number_variant','modified_bom','multi_product_revision','auto_email_in_eco'],
    'data': [
        'views/production_state.xml',
        'views/mrp_eco.xml',
        
    ],
    'demo': [
    ],
}
