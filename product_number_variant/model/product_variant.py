from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class product_variant(models.Model):
    _name = 'product.variant'
    _description = 'Product Variant' 
   
    name = fields.Char("Name", required = True)
    description = fields.Char("Description")
    sequence = fields.Integer("Sequence", required = True)
    user_id = fields.Many2one('res.users',"User",default=lambda self: self.env.user)



class product_template_inherit(models.Model):
    _inherit = 'product.template'

    
    def action_genrate_new_variant(self):
        variant_level_list = []
        if self.default_code:
            if "-" in self.default_code:
                part_char = self.default_code.split('-')[-1]
                product_variant_id = self.env['product.variant'].search([('name','=',part_char)],limit=1)

                if product_variant_id:
                    all_variant_level = self.env['product.variant'].search([])

                    for variant_level in all_variant_level:
                        variant_level_list.append(variant_level.sequence)                      
              
                else:
                    raise UserError("{0} is not a variant level that is currently maintained in the PLM app for Product Variants.".format(part_char))
                
            else:
                raise UserError("No valid current variant could be determined from this product's Part Number. A new variant cannot be generated using this method.")

            
        if variant_level_list:
            variant_level_list.sort()#sorting whole product variant sequence
            index = variant_level_list.index(product_variant_id.sequence)       
            

            if index+1 < len(variant_level_list):
                new_genrated_sequence = variant_level_list[index+1]
                seq_product_variant = self.env['product.variant'].search([('sequence','=',new_genrated_sequence)],limit=1)
                if seq_product_variant:
                    final_char = seq_product_variant.name
                    # final_part_number = self.default_code.split('-')[0]+"-"+final_char

                    split_default_code_lst = self.default_code.split('-')
                    final_part_number = ""                  
                    
                    for index in range(0,len(split_default_code_lst)-1):
                        final_part_number = final_part_number + split_default_code_lst[index] + "-"
        
                    res = self.copy()
                    res.name = self.name
                    res.default_code = final_part_number + final_char
                    new_product_id = res.id
                    default_production_state = self.env['production.state'].search([("default",'=',True)],limit=1)
                    if default_production_state:
                        res.production_state = default_production_state
                    return res.id
                                        
                    # return {
                    #         'type': 'ir.actions.act_window',
                    #         'res_model': 'product.template',
                    #         'view_type': 'form',
                    #         'view_mode': 'form',
                    #         'target': 'current',
                    #         'res_id': new_product_id,
                    #         'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}},
                    #     }                                               
                    
                    
            else:
                raise UserError("No subsequent Product Variant has been defined in the PLM app. It must be defined if you wish to generate a new Product Variant using this capability.")



            


   


                



    






