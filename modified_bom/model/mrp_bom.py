from odoo import models, fields


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    mrp_eco_product_ids = fields.One2many(
        "mrp.eco.product", "new_partline_bom_id", "Affected part to be applied"
    )
