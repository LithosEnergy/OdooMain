{
    'name': "Sales Inventory",
    'author': 'Upstackers Technologies',
    'category': 'Sales',
    'summary': """Sales Inventory""",
    'license': 'AGPL-3',
    'website': 'http://www.upstackers.com',
    'description': """
            Sales Inventory 
        """,
    'version': '13.0.0.2',
    'depends': [
                'sale_management',
                'sale_stock',
                'stock',
            ],
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/stock_approval_template_views.xml',
        'views/mail_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
