from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductionState(models.Model):
    _name = "production.state"
    _description = "Production State"

    name = fields.Char("Name", required=True, copy=False)
    description = fields.Char("Description", copy=False)
    default = fields.Boolean("Default", copy=False)
    user_id = fields.Many2one(
        "res.users", "User", default=lambda self: self.env.user, copy=False
    )

    @api.onchange("default")
    def change_default(self):
        production_states = self.env["production.state"].search(
            [("default", "=", "True")]
        )
        if production_states:
            self.default = False

    def unlink(self):
        for each in self:
            product_templates = self.env["product.template"].search(
                [("production_state", "=", each.id)]
            )
            if product_templates:
                raise UserError(
                    _(
                        "This Production State cannot be deleted because it is currently assigned to at least one product."
                    )
                )
        return super(ProductionState, self).unlink()
