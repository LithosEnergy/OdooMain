# -*- coding: utf-8 -*-
{
    'name': "Modified bom",

    'summary': """
     Modifications to the ECO Type "Bill of Materials"
       """,

    'description': """
        Modifications to the ECO Type "Bill of Materials"
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'Manufacturing',
    'version': '13.0.0',
    'depends': ['base','mrp_plm', 'purchase_stock','product_sequence_generator','product_number_variant','multi_product_revision'],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_eco.xml',
        'wizard/bom_document_wizard.xml',
        'views/product_revision.xml',
        'views/mrp_eco_stage.xml',
        'wizard/mrp_bom_line_wizard.xml',
    ],
    'qweb': [
        "static/src/xml/template.xml",
    ],
    'demo': [
    ],
}
