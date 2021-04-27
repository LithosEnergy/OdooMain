from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from urllib.parse import urlencode


class Inherit_MRP_Eco_Product(models.Model):
    _inherit = 'mrp.eco.product'

    new_partline_bom_id = fields.Many2one('mrp.bom', 'New Bill of Materials',copy=False)
    new_partline_bom_revision = fields.Integer(related='new_partline_bom_id.version', store=True, readonly=False)
    is_ecotype_bom = fields.Boolean(string="Is ECO Type BOM", default=False)
    is_bomid_for_current_line = fields.Boolean(string="Is BOM id available for cuurent line", default=False)

    # this below field is used for button action_new_revision_for_partline to handle autorun from js
    action_new_revision_depend = fields.Boolean(string="action_new_revision_depend", default=True)

    def open_new_bom_for_orderline(self):
         if self:
            if self.new_partline_bom_id:
                # self.ensure_one()
                return {
                    'name': _('Eco BoM'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'mrp.bom',
                    'target': 'current',
                    'res_id': self.new_partline_bom_id.id,
                    'context': dict(default_product_tmpl_id=self.affected_product_id.id, default_product_id=self.affected_product_id.product_variant_id.id)}
    # def open_new_bom_for_orderline(self):
    #     base_url = self.env["ir.config_parameter"].get_param("web.base.url")
    #     url_params = {
    #         'id': self.new_partline_bom_id.id,
    #         'view_type': 'form',
    #         'model': 'mrp.bom',
    #         'target':'new',

    #     }
    #     params = '/web?#%s' % urlencode(url_params)
    #     return base_url + params


    @api.onchange("affected_product_id")  
    def check_eco_type(self):
        if self.mrp_eco_id.type == 'bom':
            self.is_ecotype_bom = True

    def action_new_revision_for_partline(self):
        if (not self.is_bomid_for_current_line) and (self.generate_revision):
            if not self.action_new_revision_depend:
                if self.affected_product_id:
                    if not self.affected_product_id.bom_ids:
                        vals = {
                            'product_tmpl_id':self.affected_product_id.id,
                            'product_qty':1,
                            'version':1,
                            'active':False,
                        }
                        bom_create = self.affected_product_id.bom_ids.create(vals)
                        self.new_partline_bom_id = bom_create.id
                        self.is_bomid_for_current_line = True
                    else:
                        bom_list = []
                        for line in self.affected_product_id.bom_ids:
                            bom_list.append({'id':line.id,'version':line.version})

                        maxVerionItem = max(bom_list, key=lambda x:x['version'])

                        # vals = {
                        #     'product_tmpl_id':self.affected_product_id.id,
                        #     'product_qty':1,
                        #     'version':maxVerionItem['version']+1,
                        #     'active':False,
                        # }
                        # bom_create = self.affected_product_id.bom_ids.create(vals)

                        bom_create = self.affected_product_id.bom_ids[0].copy()
                        bom_create.version = maxVerionItem['version']+1
                        bom_create.active = False
                        self.new_partline_bom_id = bom_create.id
                        self.is_bomid_for_current_line = True
            self.action_new_revision_depend = False 


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    mrp_eco_product_ids = fields.One2many('mrp.eco.product', 'new_partline_bom_id', 'Affected part to be applied')
