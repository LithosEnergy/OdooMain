from odoo import models, fields


class inheritMrpEcoStage(models.Model):
    _inherit = "mrp.eco.stage"

    auto_e_mail = fields.Boolean(string="Auto E-mail")
    email_template = fields.Many2one("mail.template", "E-mail Template")
