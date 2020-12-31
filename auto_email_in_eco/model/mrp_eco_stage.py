from odoo import models, fields, api, _
from odoo.exceptions import UserError

class inherit_MrpEcoStage(models.Model):
    _inherit = 'mrp.eco.stage'

    auto_e_mail = fields.Boolean(string="Auto E-mail")
    email_template = fields.Many2one('mail.template',"E-mail Template")


    def write(self, vals):
        res = super(inherit_MrpEcoStage, self).write(vals) 
        if self.auto_e_mail:
            if not self.email_template:
                raise UserError(_('Please select E-Mail Template.'))       
        return res
