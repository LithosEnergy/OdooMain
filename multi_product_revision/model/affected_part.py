from odoo import models, fields, _
from odoo.exceptions import UserError


class InheritedMrpEco(models.Model):
    _inherit = "mrp.eco"

    affected_part_line = fields.One2many(
        "mrp.eco.product", "mrp_eco_id", string="Affected Part"
    )

    def action_apply(self):
        eco = super(InheritedMrpEco, self).action_apply
        if self.type == "product":
            if not self.affected_part_line:
                raise UserError(
                    _(
                        "At least one product must be specified"
                        " for this type of ECO."
                    )
                )
            if self.affected_part_line:
                for line in self.affected_part_line:
                    if not (line.generate_revision or line.production_state):
                        raise UserError(
                            _(
                                "You must specify a new Production State or"
                                " that a new Revision is to be generated for"
                                " all products on the 'Affected Parts' tab"
                                " before applying changes for this ECO."
                            )
                        )
                    else:
                        if line.production_state:
                            line.affected_product_id.production_state = (
                                line.production_state
                            )

                        if line.generate_revision:
                            if line.next_revision:
                                line.affected_product_id.version = (
                                    line.next_revision
                                )

                            wizard_line_lst = []
                            for wizard_line in line.document_wizard_line:
                                wizard_line_lst.append(
                                    (
                                        0,
                                        0,
                                        {"item_number":
                                            wizard_line.item_number,
                                         "upload_document_name":
                                             wizard_line.upload_document_name,
                                         "upload_document":
                                             wizard_line.upload_document,
                                         "full_url":
                                             wizard_line.full_url,
                                         },
                                    )
                                )
                            vals = {
                                "revision": line.affected_product_id.version,
                                "notes": line.notes,
                            }
                            line.affected_product_id.write(
                                {"product_revision_line": [(0, 0, vals)]}
                            )
                            line.affected_product_id.product_revision_line[
                                -1
                            ].document_wizard_line = wizard_line_lst

        return eco
