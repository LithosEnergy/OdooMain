from odoo import models, fields


class MrpBomLineWizard(models.TransientModel):
    _name = "mrp.bom.line.wizard"
    _description = "Mrp Bom Line Wizard"

    affected_product_id = fields.Many2one("product.template", string="Product")
    # production_state = fields.Char(
    #     related="affected_product_id.production_state.name",
    #     string="Production State")
    production_state = fields.Many2one(
        "production.state", string="Production State"
    )
    status = fields.Char(string="Status")
    eco_id_for_bom_line_wizard = fields.Many2one(
        "mrp.eco", string="Mrp Eco for bom line wizard"
    )
    selected_product = fields.Boolean(default=False)
    is_product_available_in_eco = fields.Boolean(
        string="Is product available in eco", default=False
    )
    is_changed_production_state = fields.Boolean(
        string="Is changed production state", default=False
    )
