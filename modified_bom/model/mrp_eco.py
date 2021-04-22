from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class mrp_eco(models.Model):
    _inherit = 'mrp.eco'
    
    bom_document_wizard_line = fields.One2many('bom.document.wizard','bom_mrp_eco',string="Upload Documention", store=True)
    revision_notes = fields.Char(string="Revision Notes")
    copy_eco_production_state = fields.Char(related="product_tmpl_id.production_state.name",string="Copy ECO Production State")
    eco_production_state = fields.Many2one('production.state',string="Production State")



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

        # new changes as per update to modified_bom
        if self.type == "bom":
            if not self.affected_part_line:
                raise Warning(_("At least one product must be specified for this type of ECO."))
            if self.affected_part_line:
                for line in self.affected_part_line:
                    if not(line.generate_revision or line.production_state):
                        raise Warning(_("You must specify a new Production State or that a new Revision is to be generated for all products on the 'Affected Parts' tab before applying changes for this ECO."))
                    else:
                        if line.production_state:
                            line.affected_product_id.production_state = line.production_state                                              

                        if line.generate_revision:                            
                            if line.next_revision:
                                line.affected_product_id.version = line.next_revision

                            wizard_line_lst = []
                            for wizard_line in line.document_wizard_line:
                                wizard_line_lst.append((0, 0, {
                                    'item_number': wizard_line.item_number,
                                    'upload_document_name':wizard_line.upload_document_name,
                                    'upload_document':wizard_line.upload_document,
                                    'full_url':wizard_line.full_url,
                                }))
                            vals = {
                                'revision':line.affected_product_id.version,
                                'notes':line.notes
                            }
                            line.affected_product_id.write({'product_revision_line':[(0,0,vals)]})
                            line.affected_product_id.product_revision_line[-1].document_wizard_line =  wizard_line_lst


            if self.eco_production_state:
                self.product_tmpl_id.production_state = self.eco_production_state

                if self.bom_id.bom_line_ids:                    
                    for record in self.bom_id.bom_line_ids:
                        record.product_tmpl_id.production_state = self.eco_production_state              

                    if self.affected_part_line:
                        for line in self.affected_part_line:
                            if line.affected_product_id:
                                if line.production_state:                                
                                        bom_id_product_tmpl_list = []
                                        for record in self.bom_id.bom_line_ids:
                                            bom_id_product_tmpl_list.append(record.product_tmpl_id.id)

                                        if line.affected_product_id.id in bom_id_product_tmpl_list:
                                            line.affected_product_id.production_state = line.production_state

            if self.affected_part_line:
                for line in self.affected_part_line:
                    if line.new_partline_bom_id:                        
                        if line.affected_product_id.bom_ids:
                            for bom_id in line.affected_product_id.bom_ids:
                                bom_id.active = False                        
                        line.new_partline_bom_id.active = True


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

  





