from odoo import models, fields, api, _
from odoo.exceptions import UserError


class MRPEcoProduct(models.Model):
    _name = "mrp.eco.product"
    _description = "MRP Eco Product"

    affected_product_id = fields.Many2one("product.template", string="Product")
    generate_revision = fields.Boolean(string="Generate Revision")
    generate_revision_depend = fields.Boolean(
        string="Generate Revision depend", default=False
    )
    next_revision = fields.Integer(string="Next Revision")
    notes = fields.Text(string="Notes")
    mrp_eco_id = fields.Many2one("mrp.eco", string="Mrp Eco Id")
    document_wizard_line = fields.One2many(
        "document.wizard",
        "mrp_eco_product_id",
        string="Upload Document",
        store=True,
    )

    # next revision calculation
    @api.onchange("generate_revision")
    def change_affected_product_id(self):
        if self.generate_revision:
            self.next_revision = self.affected_product_id.version + 1
            self.generate_revision_depend = True

        if not self.generate_revision:
            if self.document_wizard_line:
                raise UserError(
                    _(
                        "Documents have already been uploaded for this"
                        "new revision. You must first delete those"
                        " documents before unchecking the 'Generate"
                        " Revision' checkbox."
                    )
                )
            self.next_revision = 0

    copy_production_state = fields.Char(
        related="affected_product_id.production_state.name",
        string="Copy Production State",
    )
    production_state = fields.Many2one(
        "production.state", string="Production State"
    )

    def upload_doc(self):
        if self:
            if not self.generate_revision_depend:
                return {
                    "name": _("Upload Document"),
                    "view_mode": "form",
                    "res_model": "mrp.eco.product",
                    "type": "ir.actions.act_window",
                    "target": "new",
                    "res_id": self.id,
                    "context": {},
                }
            self.generate_revision_depend = False

    def add_document(self):
        print("Done")
