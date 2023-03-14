# -*- coding: utf-8 -*-
{
    "name": "multi product revision",
    "summary": """
     Revising multiple products via a PLM ECO
       """,
    "description": """
        Revising multiple products via a PLM ECO
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "Manufacturing",
    "version": "15.0.0.1.2",
    "license" : "OPL-1",
    "depends": [
        "base",
        "mrp_plm",
        "purchase_stock",
        "product_sequence_generator",
        "product_number_variant",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/document_wizard.xml",
        "views/multi_pro_revision.xml",
        "views/affected_part.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "multi_product_revision/static/src/js/list_renderer.js"
        ]
    },
    # 'qweb': [
    #     "static/src/xml/template.xml",
    # ],
    "demo": [],
}
