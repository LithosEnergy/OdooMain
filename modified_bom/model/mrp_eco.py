from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class mrp_eco(models.Model):
    _inherit = 'mrp.eco'
    
    bom_document_wizard_line = fields.One2many('bom.document.wizard','bom_mrp_eco',string="Upload Documention", store=True)
    revision_notes = fields.Char(string="Revision Notes")

    def upload_doc(self):        
    	view_id = self.env.ref('modified_bom.mrp_eco_wizard_form').id
    	context = self._context.copy()
    	return {
            'name':'Upload Documention',
            'view_type':'form',
            'view_mode':'tree',
            'views' : [(view_id,'form')],
            'res_model':'mrp.eco',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'res_id':self.id,
            'target':'new',
            'context':context,
        }

    def add_document(self):
        print("Done")        

    def action_apply(self):
        eco = super(mrp_eco, self).action_apply()
        if self.type == "bom":
            if self.bom_document_wizard_line:                
                bom_wizard_line_list = []
                for line in self.bom_document_wizard_line:
                    bom_wizard_line_list.append((0, 0, {
                                        'item_number': line.bom_item_number,
                                        'upload_document_name':line.bom_upload_document_name,
                                        'upload_document':line.bom_upload_document,
                                        'full_url':line.bom_full_url,
                                        'bom_document_wizard_test':True,
                                    }))

                # self.product_tmpl_id.version = self.product_tmpl_id.version #product verison incremented in base automatically
                vals = {
                        'revision':self.product_tmpl_id.version,
                        'notes':self.revision_notes
                    }
                self.product_tmpl_id.write({'product_revision_line':[(0,0,vals)]})              

                self.product_tmpl_id.product_revision_line[-1].document_wizard_line =  bom_wizard_line_list

        return eco

    # Automatically move approved ECOs
    def approve(self):
        res = super(mrp_eco, self).approve()        
        if self.approval_ids:
            if self.allow_change_stage:
                total_stages_list = self.stage_id.search([]).ids
                index_number = total_stages_list.index(self.stage_id.id)
                next_stage_id = total_stages_list[index_number+1]
                next_stage_obj = self.stage_id.search([('id','=',next_stage_id)], limit=1)
                self.stage_id = next_stage_obj                

        return res

  





