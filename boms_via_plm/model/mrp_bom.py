from odoo import models, fields


class InheritMrpBom(models.Model):
    _inherit = "mrp.bom"

    component_count = fields.Integer(
        string="Component Count", compute="_component_count"
    )

    def _component_count(self):

        for i in self:
            count = len(i.bom_line_ids)
            i.component_count = count
