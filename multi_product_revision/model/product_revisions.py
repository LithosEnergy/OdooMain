from odoo import models, fields, _


class ProductRevisions(models.Model):
    _name = "product.revisions"
    _description = "Product Revisions"

    user_id = fields.Many2one(
        "res.users", "User", default=lambda self: self.env.user
    )
    date_creation = fields.Date(
        "Created Date", required=True, default=fields.Date.today()
    )
    revision = fields.Integer(string="Revision")
    notes = fields.Text(string="Notes")

    product_template_id = fields.Many2one(
        "product.template", string="Product Template ID"
    )
    document_wizard_line = fields.One2many(
        "document.wizard",
        "product_revisions_id",
        string="Upload Documents",
        store=True,
    )

    def upload_doc(self):
        if self:
            return {
                "name": _("Upload Document"),
                "view_mode": "form",
                "res_model": "product.revisions",
                "type": "ir.actions.act_window",
                "target": "new",
                "res_id": self.id,
                "context": {},
            }
