from odoo import models, fields, api


class Bom_Document_Wizard(models.Model):
    _name = "bom.document.wizard"
    _description = "Bom Document Wizard"

    bom_item_number = fields.Integer(string="Item")
    bom_upload_document_name = fields.Char(string="Upload Document Name")
    bom_upload_document = fields.Binary(string="Upload Document")
    bom_full_url = fields.Char(string="URL", compute="_compute_full_url")
    bom_mrp_eco = fields.Many2one("mrp.eco", string="Mrp Eco")

    @api.onchange("bom_upload_document")
    def _compute_full_url(self):
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        )
        for record in self:
            record.bom_full_url = (
                "%s/web/image?model=bom.document.wizard&id=%s&"
                "field=bom_upload_document" % (base_url, record.id)
            )
