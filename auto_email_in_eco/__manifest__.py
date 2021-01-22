# -*- coding: utf-8 -*-
{
    'name': "Auto E-Mail In ECO",

    'summary': """
     Auto-e-mail on PLM ECO Stage
       """,

    'description': """
        Auto-e-mail on PLM ECO Stage.The system generates an e-mail to be sent to all these unique approvers using the e-mail template specified in the "E-mail Template" field on the ECO Stage.
    """,
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'category': 'Manufacturing',
    'version': '13.0.0',
    'depends': ['base','mrp_plm', 'purchase_stock','product_sequence_generator','product_number_variant','modified_bom','multi_product_revision'],
    'data': [
        'report/eco_report.xml',
        'views/mrp_eco_stage.xml',
        'views/eco_mail_template.xml',
        
    ],
    'demo': [
    ],
}
