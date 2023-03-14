from odoo import models, _
import base64
from urllib.parse import urlencode


class inherit_MrpEco(models.Model):
    _inherit = "mrp.eco"

    def write(self, vals):
        for rec in self:
            res = super(inherit_MrpEco, rec).write(vals)
            if vals.get("stage_id"):
                rec.send_mail_to_approvers()
            return res

    def send_mail_to_approvers(self):
        if self.stage_id.name != "New" and self.stage_id.auto_e_mail:
            company = self.env.user.company_id
            admin = self.env.user
            email_from_usr = admin.name
            email_from_mail = admin.email
            base_context = self.env.context
            mail_template = self.stage_id.email_template
            print("\n\n\n mail_template:", mail_template)
            email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {
                "email_from_usr": email_from_usr,
                "email_from_mail": email_from_mail,
            }

            email_to_list = []
            for user_id in self.stage_id.approval_template_ids.mapped(
                "user_ids"
            ):
                # for approval_id in stage_id.approval_template_ids:
                #     for user_id in approval_id.user_ids:
                # email_to_user = user_id.name
                email_to = user_id.email
                email_to_list.append(email_to)

            nondupli_email_to_list = []
            [
                nondupli_email_to_list.append(x)
                for x in email_to_list
                if x not in nondupli_email_to_list
            ]

            template = mail_template.sudo().with_context(
                base_context,
                eco_summuary_name=self.name,
                eco_stage_name=self.stage_id.name,
                email_from_usr=email_from_usr,
                email_from_mail=email_from_mail,
                # email_to_user = email_to_user,
                # company = company.logo,
                company_name=company.name,
                company_phone=company.phone or "",
                company_email=company.email or "",
                company_website=company.website or "",
                email_from=email_from,
                email_to=",".join(nondupli_email_to_list),
                subject=("ECO (Ref {})".format(self.name)),
            )
            template.send_mail(self.id, force_send=True)

            eco_report_attachment_id = self.convert_report2attachment()
            self.message_post(
                message_type=_("comment"),
                body=_(
                    """<p>Hello,</p>\n\n<p>Engineering Change Order
                    <strong>({})</strong> has been moved to stage
                    <strong>{}</strong>.</p><p>You can reply to this
                email if you have any questions.</p>\n\n<p>Thank
                you,</p><p>{}</p>""".format(
                        self.name, self.stage_id.name, email_from_usr
                    )
                ),
                attachment_ids=[eco_report_attachment_id.id],
            )

    def get_full_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].get_param("web.base.url")
        url_params = {"id": self.id, "view_type": "form", "model": "mrp.eco"}
        params = "/web?#%s" % urlencode(url_params)
        return base_url + params

    def convert_report2attachment(self):
        content = self.env.ref(
            "auto_email_in_eco.action_report_mrp_eco"
        )._render_qweb_pdf(self.ids)
        return self.env["ir.attachment"].create(
            {
                "name": self.name + ".pdf",
                "type": "binary",
                "datas": base64.encodebytes(content[0]),
                "res_model": self._name,
                "res_id": self.id,
            }
        )
