# -*- coding: utf-8 -*-
{
    "name": "Product Number Variant",
    "summary": """
     Product Number Variant Generate in Internal Reference
       """,
    "description": """
        Product Number Variant Generate in Internal Reference
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "Manufacturing",
    "version": "15.0.0.0.0",
    "license" : "OPL-1",
    "depends": [
        "base",
        "mrp_plm",
        "purchase_stock",
        "product_sequence_generator",
    ],
    "data": ["security/ir.model.access.csv", "views/product_variant.xml"],
    "demo": [],
}
