from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


# class Document_Wizard(models.TransientModel):
class Document_Wizard(models.Model):
    _name = 'document.wizard'
    _description = 'Document Wizard'

    item_number = fields.Integer(string="Item")
    upload_document_name = fields.Char(string="Upload Document Name")
    upload_document = fields.Binary(string="Upload Document")
    mrp_eco_product_id = fields.Many2one('mrp.eco.product',string='Mrp Eco Product Id')
    full_url = fields.Char(string="URL", compute='_compute_full_url')
    product_revisions_id = fields.Many2one('product.revisions',string='Product Revisions Id')


    def create(self, vals_list):
        active_id = self.env['mrp.eco.product'].browse(self._context.get('active_ids', [])).id
        for val in vals_list:
            if 'bom_document_wizard_test' in val:#for type bom
                val.pop('bom_document_wizard_test')
            else:
                val['mrp_eco_product_id'] = active_id #for type product          
        lines = super(Document_Wizard,self).create(vals_list)     
        return lines


    @api.onchange('upload_document')
    def _compute_full_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")   
        for record in self:
            record.full_url = "%s/web/image?model=document.wizard&id=%s&field=upload_document" % (base_url, record.id)


