from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class inherited_mrp_eco(models.Model):
    _inherit = 'mrp.eco'

    affected_part_line = fields.One2many('mrp.eco.product','mrp_eco_id',string="Affected Part")
    # for_call_write = fields.Boolean(string="click me before save")
    
    # def write(self, vals):    
    #     eco = super(inherited_mrp_eco, self).write(vals)
    #     if self.type == "product":
    #         if not self.affected_part_line:
    #             raise Warning(_("At least one product must be specified for this type of ECO."))
    #         if self.affected_part_line:
    #             for line in self.affected_part_line:
    #                 if not(line.generate_revision or line.production_state):
    #                     raise Warning(_("You must specify a new Production State or that a new Revision is to be generated for all products on the 'Affected Parts' tab before applying changes for this ECO."))
    #                 else:
    #                     if line.production_state:
    #                         line.affected_product_id.production_state = line.production_state
    #                     if line.next_revision:
    #                         line.affected_product_id.version = line.next_revision

    #                     if line.generate_revision:                   
                            

    #                         revision_lst = []
    #                         for revision_line in line.affected_product_id.product_revision_line:
    #                             revision_lst.append(revision_line.revision)
    #                         if line.next_revision in revision_lst:  
    #                             for revision_line in line.affected_product_id.product_revision_line:
    #                                 if line.next_revision == revision_line.revision:                   


    #                                     wizard_line_lst = []
    #                                     for wizard_line in line.document_wizard_line:
    #                                         wizard_line_lst.append((0, 0, {
    #                                             'item_number': wizard_line.item_number,
    #                                             'upload_document_name':wizard_line.upload_document_name,
    #                                             'upload_document':wizard_line.upload_document,
    #                                             'full_url':wizard_line.full_url,
    #                                         }))

    #                                     vals = {
    #                                         'revision':line.affected_product_id.version,
    #                                         # 'document_wizard_line':wizard_line_lst,
    #                                         'notes':line.notes
    #                                     }
    #                                     # line.affected_product_id.update({'product_revision_line':[(0,0,vals)]})
    #                                     revision_line.revision = vals['revision']
    #                                     revision_line.notes = vals['notes']
    #                                     revision_line.document_wizard_line.unlink()
    #                                     revision_line.document_wizard_line = wizard_line_lst
    #                                     # line.affected_product_id.product_revision_line[-1].document_wizard_line =  wizard_line_lst
    #                         else:
    #                             wizard_line_lst = []
    #                             for wizard_line in line.document_wizard_line:
    #                                 wizard_line_lst.append((0, 0, {
    #                                     'item_number': wizard_line.item_number,
    #                                     'upload_document_name':wizard_line.upload_document_name,
    #                                     'upload_document':wizard_line.upload_document,
    #                                     'full_url':wizard_line.full_url,
    #                                 }))

    #                             vals = {
    #                                 'revision':line.affected_product_id.version,
    #                                 # 'document_wizard_line':wizard_line_lst,
    #                                 'notes':line.notes
    #                             }
    #                             line.affected_product_id.write({'product_revision_line':[(0,0,vals)]})
    #                             line.affected_product_id.product_revision_line[-1].document_wizard_line =  wizard_line_lst




        
        # return eco

    def action_apply(self):
        eco = super(inherited_mrp_eco, self).action_apply()

        if self.type == "product":
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

        return eco


    

class MRP_Eco_Product(models.Model):
    _name = 'mrp.eco.product'
    _description = 'MRP Eco Product'    

    affected_product_id = fields.Many2one('product.template', string="Product")
    generate_revision = fields.Boolean(string="Generate Revision")
    next_revision = fields.Integer(string="Next Revision")
    notes = fields.Text(string="Notes")
    mrp_eco_id = fields.Many2one('mrp.eco',string='Mrp Eco Id')
    document_wizard_line = fields.One2many('document.wizard','mrp_eco_product_id',string="upload doc", store=True,)


   
    # next revision calculation
    @api.onchange("generate_revision")    
    def change_affected_product_id(self):
        if self.generate_revision:            
            self.next_revision = self.affected_product_id.version + 1
        if not self.generate_revision:
            if self.document_wizard_line:
                raise Warning(_("Documents have already been uploaded for this new revision. You must first delete those documents before unchecking the 'Generate Revision' checkbox."))
            self.next_revision = 0
        # vals = {'affected_part_line':self}
        # self.mrp_eco_id.write(vals)      
        
           
 


    # # production_state which is not assigned to any product
    # def onchange_production_state(self):
    #     product_states = []
    #     production_temps = self.env['product.template'].search([])
    #     if production_temps:
    #         for temp in production_temps:
    #             if temp.production_state:
    #                 product_states.append(temp.production_state)

    #     production_states = self.env['production.state'].search([])
    #     final_return_state_list = []
    #     for state in production_states:
    #         if state not in product_states:                
    #             final_return_state_list.append(state.id)
    #     return [('id','in',final_return_state_list)]    



    @api.onchange('affected_product_id') 
    def onchange_production_state(self): 
        res = {}
        if self.affected_product_id:
            res['domain'] = {'production_state': [('id', '!=', self.affected_product_id.production_state.id)]}
        print("res",res)
        return res    



    # production_state = fields.Many2one('production.state',string="Production State", domain=onchange_production_state)
    production_state = fields.Many2one('production.state',string="Production State")


  
    def upload_doc(self):
        if self:
            return {
            'name': _('Upload Document'),
            'view_mode': 'form',
            'res_model': 'mrp.eco.product',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id':self.id,
            'context': {},
        }

    def add_document(self):
        print("Done")   

    



    
        





            


   