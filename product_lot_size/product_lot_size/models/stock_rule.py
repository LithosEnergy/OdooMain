# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
from collections import defaultdict


class StockRule(models.Model):
    _inherit = 'stock.rule'


    @api.model
    def _run_manufacture(self, procurements):
        """
        This method is over written as it is called from scheduler
        which will divide the quantity of product as per the lot 
        size set on the product and eventually create all MO according 
        to the lot size."""
        productions_values_by_company = defaultdict(list)
        for procurement, rule in procurements:
            bom = self._get_matching_bom(procurement.product_id, procurement.company_id, procurement.values)
            if not bom:
                msg = _('There is no Bill of Material of type manufacture or kit found for the product %s. Please define a Bill of Material for this product.') % (procurement.product_id.display_name,)
                raise UserError(msg)
        # Logic which divides the maximum quantity on Reordering Rule with
        # lot size of product.
        if procurement.product_id.product_lot_size > 0:
            
            qty_list = []
            divided_qty = int(procurement.product_qty / procurement.product_id.product_lot_size)  # 3
            modulo_qty = procurement.product_qty % procurement.product_id.product_lot_size  # 1

            for i in range(int(divided_qty)):
                qty_list.append(procurement.product_id.product_lot_size)
            if modulo_qty > 0:
                qty_list.append(modulo_qty)
            
            for each_qty in qty_list:
                productions = self.env['mrp.production'].sudo().with_context(force_company=procurement.company_id.id).create(self._prepare_mo_vals(*procurement, bom))
                productions.write({'product_qty':each_qty})
                self.env['stock.move'].sudo().create(productions._get_moves_raw_values())
                productions.action_confirm()

                for production in productions:
                    origin_production = production.move_dest_ids and production.move_dest_ids[0].raw_material_production_id or False
                    orderpoint = production.orderpoint_id
                    if orderpoint:
                        production.message_post_with_view('mail.message_origin_link',
                                                          values={'self': production, 'origin': orderpoint},
                                                          subtype_id=self.env.ref('mail.mt_note').id)
                    if origin_production:
                        production.message_post_with_view('mail.message_origin_link',
                                                          values={'self': production, 'origin': origin_production},
                                                          subtype_id=self.env.ref('mail.mt_note').id)

        else:

            productions_values_by_company[procurement.company_id.id].append(rule._prepare_mo_vals(*procurement, bom))

            for company_id, productions_values in productions_values_by_company.items():
                # create the MO as SUPERUSER because the current user may not have the rights to do it (mto product launched by a sale for example)
                productions = self.env['mrp.production'].sudo().with_context(force_company=company_id).create(productions_values)
                self.env['stock.move'].sudo().create(productions._get_moves_raw_values())
                productions.action_confirm()

                for production in productions:
                    origin_production = production.move_dest_ids and production.move_dest_ids[0].raw_material_production_id or False
                    orderpoint = production.orderpoint_id
                    if orderpoint:
                        production.message_post_with_view('mail.message_origin_link',
                                                          values={'self': production, 'origin': orderpoint},
                                                          subtype_id=self.env.ref('mail.mt_note').id)
                    if origin_production:
                        production.message_post_with_view('mail.message_origin_link',
                                                          values={'self': production, 'origin': origin_production},
                                                          subtype_id=self.env.ref('mail.mt_note').id)
        return True
