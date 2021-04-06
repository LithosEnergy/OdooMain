from odoo import models,fields,api


class SaleOrder(models.Model):
    _inherit ="sale.order"

    project_code=fields.Text(string="Project Code")

    @api.model
    def action_confirm(self):
        record = super(SaleOrder, self).action_confirm()
        mo=self.env['mrp.production'].search([('origin','=',self.name)])
        for line in mo:
            line.project_code=self.project_code
        return record


