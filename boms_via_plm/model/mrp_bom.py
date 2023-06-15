from odoo import models, fields


class InheritMrpBom(models.Model):
    _inherit = "mrp.bom"

    component_count = fields.Integer(
        string="Component Count", compute="_component_count"
    )
    # New field added for production state
    production_state_id = fields.Many2one(
        "production.state",
        related="product_tmpl_id.production_state",
        string="Production State")

    def _component_count(self):
        for i in self:
            count = len(i.bom_line_ids)
            i.component_count = count
