# -*- coding: utf-8 -*-

{
    'name': 'Clear to Build Report',
    'version': '13.0.1.1',
    'summary': 'Clear to Build Report',
    'author': "S4 Solutions, LLC",
    'website': "https://www.sfour.io/",
    'sequence': 1,
    'description': """
        Clear to Build Report
    """,
    'category': 'mrp',
    'images': [],
    'depends': ['base', 'purchase','mrp','mrp_plm'],
    'data': [
        'views/mrp_templates.xml',
        'views/stock_location_views.xml',        
        'report/mrp_report_bom_structure.xml',
    ],
    'qweb': ['static/src/xml/mrp.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}

