# -*- coding: utf-8 -*-

{
    "name": "Clear to Build Report",
    "version": "15.0.0.0.0",
    "summary": "Clear to Build Report",
    "author": "S4 Solutions, LLC",
    "website": "https://www.sfour.io/",
    "sequence": 1,
    "description": """
        Clear to Build Report
    """,
    "category": "mrp",
    "images": [],
    "depends": ["base", "purchase", "mrp", "mrp_plm"],
    "data": [
        "views/stock_location_views.xml",
        "report/mrp_report_bom_structure.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "clear_to_build_report/static/src/js/mrp_bom_report.js"
        ]
    },
    "qweb": ["static/src/xml/mrp.xml"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
