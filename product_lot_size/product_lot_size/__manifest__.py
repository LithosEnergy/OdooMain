# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Lot Size',
    'version': '13.0.1.0.0',
    'author': "Aktiv Software",
    'license': "AGPL-3",
    'website': "http://www.aktivsoftware.com",
    'category': 'mrp',
    'depends': ['stock', 'mrp'],
    'summary': 'The module delivers a facility of creating multiple Manufacturing Orders (MO) as per the size set on the Product.',
    'data': [
            'views/product_views.xml',
            ],
    'installable': True,
    'auto_install': False,
}
