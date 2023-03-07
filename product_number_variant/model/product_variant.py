from odoo import models, fields


class ProductVariant(models.Model):
    _name = "product.variant"
    _description = "Product Variant"

    name = fields.Char("Name", required=True)
    description = fields.Char("Description")
    sequence = fields.Integer("Sequence", required=True)
    user_id = fields.Many2one(
        "res.users", "User", default=lambda self: self.env.user
    )
