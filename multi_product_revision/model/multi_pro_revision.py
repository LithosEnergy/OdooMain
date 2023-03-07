from odoo import models, fields


class InheritedMrpEco(models.Model):
    _inherit = "product.template"

    product_revision_line = fields.One2many(
        "product.revisions", "product_template_id", string="Product Revisions"
    )
