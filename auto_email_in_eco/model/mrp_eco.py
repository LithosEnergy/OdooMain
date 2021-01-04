from odoo import models, fields, api, _


class inherit_MrpEco(models.Model):
    _inherit = 'mrp.eco'
    

    def write(self, vals):
        res = super(inherit_MrpEco, self).write(vals)
        if vals.get('stage_id'):
            self.send_mail_to_approvers()
        return res

    def send_mail_to_approvers(self):
        if self:
            if self.stage_id.name != "New":               
                if self.stage_id.auto_e_mail == True:
                    current_user = self.env.user.id
                    company = self.env.user.company_id
                    admin = self.env['res.users'].search([('id','=',current_user)])
                    email_from_usr = admin.name
                    email_from_mail = admin.email           
                    base_context = self.env.context 

                    # template_id = self.env.ref('auto_email_in_eco.custom_plm_eco_email_template').id                   
                    template_id = self.stage_id.email_template.id

                    mail_template = self.env['mail.template'].browse(template_id)
                    email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}

                    email_to_list = []
                    for stage_id in self.stage_id.search([]):
                        for approval_id in stage_id.approval_template_ids:
                            for user_id in approval_id.user_ids:
                                email_to_user = user_id.name
                                email_to = user_id.email
                                email_to_list.append(email_to)

                    nondupli_email_to_list = [] 
                    [nondupli_email_to_list.append(x) for x in email_to_list if x not in nondupli_email_to_list]

                    template = mail_template.sudo().with_context(base_context,
                        eco_summuary_name = self.name,
                        eco_stage_name = self.stage_id.name,
                        email_from_usr = email_from_usr,
                        email_from_mail = email_from_mail,
                        # email_to_user = email_to_user,
                        company = company.logo,
                        email_from = email_from,
                        email_to = ",".join(nondupli_email_to_list),
                        subject = ("ECO stage is changed "),
                        )         
                    template.send_mail(self.id, force_send=True)                                      
                    self.message_post(message_type=_('comment'),body=_('''<p>Hello,</p>\n\n<p>User has changed ECO({}) stage to {}.</p>\n\n<p>Regards,</p><p>{}</p>'''.format(self.name,self.stage_id.name,email_from_usr)))                 
                    # template.send_mail(self.search([('name','=',self.name)]).id, force_send=True) #if onchange stage_id used

