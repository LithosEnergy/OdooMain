from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class inherited_mrp_eco(models.Model):
    _inherit = 'product.template'

    product_revision_line = fields.One2many('product.revisions','product_template_id',string="Product Revisions")
    

class Product_Revisions(models.Model):
    _name = 'product.revisions'
    _description = 'Product Revisions'

    user_id = fields.Many2one('res.users',"User",default=lambda self: self.env.user)
    date_creation = fields.Date('Created Date', required=True, default=fields.Date.today())
    revision = fields.Integer(string="Revision")
    notes = fields.Text(string="Notes")


    product_template_id = fields.Many2one('product.template',string='Product Template ID')
    document_wizard_line = fields.One2many('document.wizard','product_revisions_id',string="Upload Documents", store=True,)






