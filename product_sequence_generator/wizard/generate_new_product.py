
from odoo import models, fields, api, _


class Generate_Product_Wizard(models.TransientModel):
    _name = 'generate.product.wizard'
    _description = 'Generate Product Wizard'

    @api.model
    def _get_buy_route(self):
        buy_route = self.env.ref('purchase_stock.route_warehouse0_buy', raise_if_not_found=False)
        if buy_route:
            return buy_route.ids
        return []

    def _get_default_uom_id(self):
        return self.env["uom.uom"].search([], limit=1, order='id').id

    def _get_default_category_id(self):
        if self._context.get('categ_id') or self._context.get('default_categ_id'):
            return self._context.get('categ_id') or self._context.get('default_categ_id')
        category = self.env.ref('product.product_category_all', raise_if_not_found=False)
        if not category:
            category = self.env['product.category'].search([], limit=1)
        if category:
            return category.id
        else:
            err_msg = _('You must define at least one product category in order to be able to create products.')
            redir_msg = _('Go to Internal Categories')
            raise RedirectWarning(err_msg, self.env.ref('product.product_category_action_form').id, redir_msg)

    name = fields.Char("Product Description",  required=True)
    route_ids = fields.Many2many(
        'stock.location.route', 'stock_route_generate_product', 'generate_product_id', 'route_id', 'Routes',
        domain=[('product_selectable', '=', True)],
        help="Depending on the modules installed, this will allow you to define the route of the product: whether it will be bought, manufactured, replenished on order, etc.",
        default=lambda self: self._get_buy_route())
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", help="Ensure the traceability of a storable product in your warehouse.", default='none', required=True)
    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")
    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id',
        required=True, help="Select category for the current product")
    
    #Generate new product 
    def create_product(self):
        sequence = self.env['ir.sequence'].next_by_code('product.part') 
        vals = {'name': self.name,
                'type': "product",
                'route_ids': [(6, 0, self.route_ids.ids)],
                'tracking': self.tracking,
                'uom_id': self.uom_id.id,
                'uom_po_id': self.uom_id.id,
                'default_code': sequence,
                'sale_ok': False,
                'categ_id': self.categ_id.id}
        
        product = self.env['product.template'].create(vals)
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'product.template',
                'view_mode': 'form',
                'res_id': product.id,
                'target': 'current'
                }
       
            