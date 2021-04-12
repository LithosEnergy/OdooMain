from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

# class Document_Wizard(models.TransientModel):
class Document_Wizard(models.Model):
    _name = 'document.wizard'
    _description = 'Document Wizard'     

    @api.onchange('item_number')
    def _get_item_numbers(self):        
        if self:            
            first_line_rec = self[0] 
            if first_line_rec.product_revisions_id:
                for value, index in enumerate(first_line_rec.product_revisions_id.document_wizard_line, start=1):
                    index.update({'item_number':value})  
            elif first_line_rec.mrp_eco_product_id:
                for value, index in enumerate(first_line_rec.mrp_eco_product_id.document_wizard_line, start=1):
                    index.update({'item_number':value})


    item_number = fields.Integer(string="Item",compute='_get_item_numbers')
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
                # val['mrp_eco_product_id'] = active_id #for type product  
                if active_id:
                    mrp_eco_product_lst = self.env['mrp.eco.product'].search([]).ids
                    if active_id in mrp_eco_product_lst:
                        val['mrp_eco_product_id'] = active_id

        lines = super(Document_Wizard,self).create(vals_list)     
        return lines


    @api.onchange('upload_document')
    def _compute_full_url(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")   
        for record in self:
            # record.full_url = "%s/web/image?model=document.wizard&id=%s&field=upload_document" % (base_url, record.id)
            record.full_url = "%s/web/image/document.wizard/%s/upload_document/%s" % (base_url, record.id,record.upload_document_name)

