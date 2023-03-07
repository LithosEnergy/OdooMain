# -*- coding: utf-8 -*-
{
    "name": "Product Sequence Generator",
    "summary": """
     Product sequence Generate in Internal Reference
       """,
    "description": """
        Product sequence Generate in Internal Reference
    """,
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "category": "Manufacturing",
    "version": "15.0.0.0.0",
    "depends": ["base", "mrp_plm", "purchase_stock"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/generate_new_product.xml",
        "views/production_state.xml",
        "views/res_partner.xml",
        "views/product_template.xml",
        "views/mrp_eco.xml",
    ],
    "demo": ["demo/product_sequence_data.xml"],
}
