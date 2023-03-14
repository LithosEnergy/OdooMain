from odoo import models
from odoo.exceptions import (
    UserError
)


class inherit_MrpEco(models.Model):
    _inherit = "mrp.eco"

    def action_apply(self):
        eco = super(inherit_MrpEco, self).action_apply()
        if self.type == "bom":
            if self.new_bom_id:
                if self.new_bom_id.bom_line_ids:
                    for line in self.new_bom_id.bom_line_ids:
                        line_product_sequence = (
                            line.product_id.product_tmpl_id.production_state.sequence
                        )
                        bom_product_sequence = (
                            self.new_bom_id.product_tmpl_id.production_state.sequence
                        )
                        if line_product_sequence < bom_product_sequence:
                            raise UserError(
                                "Component '[{0}]{1}' is at a lower production"
                                " state than the parent product and cannot"
                                " be added to this BOM.".format(
                                    line.product_id.default_code,
                                    line.product_id.name,
                                )
                            )
        return eco

    def bom_id_create(self):
        if self.product_tmpl_id:
            if not self.product_tmpl_id.bom_ids:
                vals = {
                    "product_tmpl_id": self.product_tmpl_id.id,
                    "product_qty": 1,
                    "version": 0,
                }
                bom_create = self.product_tmpl_id.bom_ids.create(vals)
                self.bom_id = bom_create.id

    def action_new_revision(self):
        for eco in self:
            if eco.type == "bom":
                if not eco.bom_id:
                    eco.bom_id_create()
        res = super(inherit_MrpEco, self).action_new_revision()
        return res
