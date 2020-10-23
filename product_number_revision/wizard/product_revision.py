from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class product_revision(models.Model):
    _name = 'product.revision'
    _description = 'Product Revision' 
   
    name = fields.Char("Name", required = True)
    description = fields.Char("Description")
    sequence = fields.Integer("Sequence", required = True)
    user_id = fields.Many2one('res.users',"User",default=lambda self: self.env.user)


class product_template_inherit(models.Model):
    _inherit = 'product.template'

    def action_genrate_new_revision(self):
        revision_level_list = []
        if self.default_code:
            if "-" in self.default_code:
                part_char = self.default_code.split('-')[-1]
                product_revision_id = self.env['product.revision'].search([('name','=',part_char)],limit=1)

                if product_revision_id:
                    all_revision_level = self.env['product.revision'].search([])

                    for revision_level in all_revision_level:
                        revision_level_list.append(revision_level.sequence)                      
              
                else:
                    raise UserError("{0} is not a revision level that is currently maintained in the PLM app for Product Revisions.".format(part_char))
                
            else:
                raise UserError("No valid current revision could be determined from this product's Part Number. A new revision cannot be generated using this method.")

            
        if revision_level_list:
            revision_level_list.sort()#sorting whole product revision sequence
            index = revision_level_list.index(product_revision_id.sequence)       
            

            if index+1 < len(revision_level_list):
                new_genrated_sequence = revision_level_list[index+1]
                seq_product_revision = self.env['product.revision'].search([('sequence','=',new_genrated_sequence)],limit=1)
                if seq_product_revision:
                    final_char = seq_product_revision.name
                    final_part_number = self.default_code.split('-')[0]+"-"+final_char
                    res = self.copy()
                    res.name = self.name
                    res.default_code = final_part_number
            else:
                raise UserError("There is no closer sequence for this part number.")
                



    






