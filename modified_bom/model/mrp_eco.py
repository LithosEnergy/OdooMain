from odoo import models, fields, _
from odoo.exceptions import UserError


class MrpEco(models.Model):
    _inherit = "mrp.eco"

    bom_document_wizard_line = fields.One2many(
        "bom.document.wizard",
        "bom_mrp_eco",
        string="Upload Documention",
        store=True,
    )
    revision_notes = fields.Char(string="Revision Notes")
    copy_eco_production_state = fields.Char(
        related="product_tmpl_id.production_state.name",
        string="Copy ECO Production State",
    )
    eco_production_state = fields.Many2one(
        "production.state", string="Production State"
    )

    # mrp_bom_line_wizard = fields.One2many(
    #     'mrp.bom.line.wizard', 'abc',
    #     string="Mrp Bom Line Wizard")
    mrp_bom_wizard_line = fields.One2many(
        "mrp.bom.line.wizard",
        "eco_id_for_bom_line_wizard",
        string="mrp bom wizard line",
    )
    stage_id_check_production_state = fields.Boolean(
        related="stage_id.check_production_state",
        string="Current stage check production state",
    )

    def upload_doc(self):
        view_id = self.env.ref("modified_bom.mrp_eco_wizard_form").id
        context = self._context.copy()
        return {
            "name": "Upload Documention",
            "view_type": "form",
            "view_mode": "tree",
            "views": [(view_id, "form")],
            "res_model": "mrp.eco",
            "view_id": view_id,
            "type": "ir.actions.act_window",
            "res_id": self.id,
            "target": "new",
            "context": context,
        }

    def add_document(self):
        print("Done")

    def action_apply(self):
        eco = super(MrpEco, self).action_apply()
        if self.type == "bom":
            # The user does not populate a new production state
            # value and attempts to submit the ECO change then
            # show error(modified_bom2)
            if self.mrp_bom_wizard_line:
                affected_products_list_with_production_state = []
                if self.affected_part_line:
                    for line in self.affected_part_line:
                        affected_products_list_with_production_state.append(
                            {
                                "affected_product_id":
                                    line.affected_product_id.id,
                                "production_state": line.production_state,
                            }
                        )

                if affected_products_list_with_production_state:
                    for line in self.mrp_bom_wizard_line:
                        for (
                            record
                        ) in affected_products_list_with_production_state:
                            if (
                                record["affected_product_id"]
                                == line.affected_product_id.id
                            ):
                                if not record["production_state"]:
                                    raise UserError(
                                        _(
                                            "You must specify a new Production"
                                            " State or that a new Revision is"
                                            " to be generated for all products"
                                            " on the 'Affected Parts' tab"
                                            " before applying changes for"
                                            " this ECO."
                                        )
                                    )
            if self.bom_document_wizard_line:
                bom_wizard_line_list = []
                for line in self.bom_document_wizard_line:
                    bom_wizard_line_list.append(
                        (
                            0,
                            0,
                            {
                                "item_number": line.bom_item_number,
                                "upload_document_name":
                                    line.bom_upload_document_name,
                                "upload_document": line.bom_upload_document,
                                "full_url": line.bom_full_url,
                                "bom_document_wizard_test": True,
                            },
                        )
                    )

                vals = {
                    "revision": self.product_tmpl_id.version,
                    "notes": self.revision_notes,
                }
                if self.new_bom_id:
                    vals["bom_version"] = self.new_bom_id.version
                self.product_tmpl_id.write(
                    {"product_revision_line": [(0, 0, vals)]}
                )

                if bom_wizard_line_list:
                    self.product_tmpl_id.product_revision_line[
                        -1
                    ].document_wizard_line = bom_wizard_line_list

                # new changes as per update to modified_bom (requirement point7)
                if self.new_bom_id.bom_line_ids:
                    if (
                        self.eco_production_state
                    ):  # if user has add value in eco_production_state in eco
                        for record in self.new_bom_id.bom_line_ids:
                            if (
                                not self.eco_production_state.sequence
                                <= record.product_tmpl_id.production_state.sequence
                            ):
                                if not self.affected_part_line:
                                    raise UserError(
                                        _(
                                            "Please check the production state"
                                            " of components in BOM revision."
                                        )
                                    )
                                else:
                                    affected_product_tmpl_list = []
                                    for line in self.affected_part_line:
                                        if line.production_state:
                                            affected_product_tmpl_list.append(
                                                line.affected_product_id.id
                                            )
                                    if (
                                        record.product_tmpl_id.id
                                        not in affected_product_tmpl_list
                                    ):
                                        raise UserError(
                                            _(
                                                "Please check the production state"
                                                " of components in BOM revision."
                                            )
                                        )

                        if self.affected_part_line:
                            for line in self.affected_part_line:
                                if line.affected_product_id:
                                    new_bom_id_product_tmpl_list = []
                                    for record in self.new_bom_id.bom_line_ids:
                                        new_bom_id_product_tmpl_list.append(
                                            record.product_tmpl_id.id
                                        )
                                    if (
                                        line.affected_product_id.id
                                        in new_bom_id_product_tmpl_list
                                    ):
                                        if line.production_state:
                                            # the production_state of products
                                            # should be same or greater level than
                                            # production state of header level
                                            # production state
                                            if (
                                                not line.production_state.sequence
                                                >= self.eco_production_state.sequence
                                            ):
                                                raise UserError(
                                                    _(
                                                        "Please check the"
                                                        " production state of"
                                                        " product '[%s]%s' in"
                                                        " Affected Parts."
                                                        % (
                                                            line.affected_product_id.default_code,
                                                            line.affected_product_id.name,
                                                        )
                                                    )
                                                )

                    else:  # if not value in eco_production_state in eco
                        if self.new_bom_id.product_tmpl_id.production_state:
                            for record in self.new_bom_id.bom_line_ids:
                                if (
                                    not
                                    record.product_tmpl_id.production_state.sequence
                                    >= self.new_bom_id.product_tmpl_id.production_state.sequence
                                ):
                                    if not self.affected_part_line:
                                        raise UserError(
                                            _(
                                                "Please check the production state"
                                                " of components in BOM revision."
                                            )
                                        )
                                    else:
                                        affected_product_tmpl_list = []
                                        for line in self.affected_part_line:
                                            if line.production_state:
                                                affected_product_tmpl_list.append(
                                                    line.affected_product_id.id
                                                )
                                        if (
                                            record.product_tmpl_id.id
                                            not in affected_product_tmpl_list
                                        ):
                                            raise UserError(
                                                _(
                                                    "Please check the production"
                                                    " state of components in BOM"
                                                    " revision."
                                                )
                                            )

                            if self.affected_part_line:
                                for line in self.affected_part_line:
                                    if line.affected_product_id:
                                        new_bom_id_product_tmpl_list = []
                                        for record in self.new_bom_id.bom_line_ids:
                                            new_bom_id_product_tmpl_list.append(
                                                record.product_tmpl_id.id
                                            )
                                        if (
                                            line.affected_product_id.id
                                            in new_bom_id_product_tmpl_list
                                        ):
                                            if line.production_state:
                                                # the production_state of products
                                                # should be same or greater level
                                                # than production state of header
                                                # level production state
                                                if (
                                                    not
                                                    line.production_state.sequence
                                                    >= self.new_bom_id.product_tmpl_id.production_state.sequence
                                                ):
                                                    raise UserError(
                                                        _(
                                                            "Please check the"
                                                            " production state of"
                                                            " product '[%s]%s' in"
                                                            " Affected Parts."
                                                            % (
                                                                line.affected_product_id.default_code,
                                                                line.affected_product_id.name,
                                                            )
                                                        )
                                                    )

                    # condition added if no any production state added to
                    # components in bom revision
                    for record in self.new_bom_id.bom_line_ids:
                        if not record.product_tmpl_id.production_state:
                            if not self.affected_part_line:
                                raise UserError(
                                    _(
                                        "There is no any production state to some"
                                        " of components in BOM revision."
                                    )
                                )
                            else:
                                affected_product_tmpl_list_2 = []
                                for line in self.affected_part_line:
                                    if line.production_state:
                                        affected_product_tmpl_list_2.append(
                                            line.affected_product_id.id
                                        )
                                if (
                                    record.product_tmpl_id.id
                                    not in affected_product_tmpl_list_2
                                ):
                                    raise UserError(
                                        _(
                                            "There is no any production state to"
                                            " some of components in BOM revision."
                                        )
                                    )

            if self.eco_production_state:
                self.product_tmpl_id.production_state = (
                    self.eco_production_state
                )

            if self.affected_part_line:
                for line in self.affected_part_line:
                    if not (line.generate_revision or line.production_state):
                        raise UserError(
                            _(
                                "You must specify a new Production State or"
                                " that a new Revision is to be generated for"
                                " all products on the 'Affected Parts' tab"
                                " before applying changes for this ECO."
                            )
                        )
                    else:
                        if line.production_state:
                            line.affected_product_id.production_state = (
                                line.production_state
                            )

                        if line.generate_revision:
                            if line.next_revision:
                                line.affected_product_id.version = (
                                    line.next_revision
                                )

                            wizard_line_lst = []
                            for wizard_line in line.document_wizard_line:
                                wizard_line_lst.append(
                                    (
                                        0,
                                        0,
                                        {
                                            "item_number":
                                                wizard_line.item_number,
                                            "upload_document_name":
                                                wizard_line.upload_document_name,
                                            "upload_document":
                                                wizard_line.upload_document,
                                            "full_url": wizard_line.full_url,
                                        },
                                    )
                                )
                            vals = {
                                "revision": line.affected_product_id.version,
                                "notes": line.notes,
                            }

                            if line.new_partline_bom_revision:
                                vals[
                                    "bom_version"
                                ] = line.new_partline_bom_revision

                            line.affected_product_id.write(
                                {"product_revision_line": [(0, 0, vals)]}
                            )
                            line.affected_product_id.product_revision_line[
                                -1
                            ].document_wizard_line = wizard_line_lst

            # make existed bom archived state and newly create bom in
            # active state (point7)
            if self.affected_part_line:
                for line in self.affected_part_line:
                    if line.new_partline_bom_id:
                        if line.affected_product_id.bom_ids:
                            for bom_id in line.affected_product_id.bom_ids:
                                bom_id.active = False
                        line.new_partline_bom_id.active = True

        return eco

    # Automatically move approved ECOs
    def approve(self):
        res = super(MrpEco, self).approve()
        if self.approval_ids:
            if self.allow_change_stage:
                total_stages_list = self.stage_id.search([]).ids
                index_number = total_stages_list.index(self.stage_id.id)
                if total_stages_list[-1] != total_stages_list[index_number]:
                    next_stage_id = total_stages_list[index_number + 1]
                    next_stage_obj = self.stage_id.search(
                        [("id", "=", next_stage_id)], limit=1
                    )
                    self.stage_id = next_stage_obj
        return res

    def add_product_from_wizard(self):
        if not self.new_bom_id:
            raise UserError(_("NO BOM revision available."))
        if not self.new_bom_id.product_tmpl_id.production_state:
            raise UserError(
                _("No production state avaiable for BOM product's.")
            )

        if self.mrp_bom_wizard_line:
            self.mrp_bom_wizard_line.unlink()

        mrp_bom_wizard_line_list = []
        for record in self.new_bom_id.bom_line_ids:
            if (
                not record.product_tmpl_id.production_state.sequence
                >= self.new_bom_id.product_tmpl_id.production_state.sequence
            ) or (not record.product_tmpl_id.production_state):
                mrp_bom_wizard_line_list.append(
                    (0, 0, {"affected_product_id": record.product_tmpl_id.id})
                )
        if mrp_bom_wizard_line_list:
            self.mrp_bom_wizard_line = mrp_bom_wizard_line_list

            affected_products_list = []
            affected_products_list_with_production_state = []
            if self.affected_part_line:
                for line in self.affected_part_line:
                    affected_products_list.append(line.affected_product_id.id)
                    affected_products_list_with_production_state.append(
                        {
                            "affected_product_id": line.affected_product_id.id,
                            "production_state": line.production_state,
                        }
                    )

            for line in self.mrp_bom_wizard_line:
                if (
                    line.affected_product_id.id in affected_products_list
                ):  # if wizard line product_id is available in affected
                    # part line product list
                    line.is_product_available_in_eco = True
                    line.status = "On ECO"
                else:
                    line.production_state = (
                        line.affected_product_id.production_state
                    )

                for record in affected_products_list_with_production_state:
                    if (
                        record["affected_product_id"]
                        == line.affected_product_id.id
                    ):
                        if record["production_state"]:
                            line.production_state = record["production_state"]
                            line.is_changed_production_state = True
                        else:
                            line.production_state = (
                                line.affected_product_id.production_state
                            )

        else:
            raise UserError(
                _(
                    "No components whose production states are lower than"
                    " the current BOM product's production state."
                )
            )

        view_id = self.env.ref("modified_bom.custom_mrp_eco_wizard_form").id
        return {
            "name": "The below components have production states which"
                    " are lower than production state of product "
                    " '[{}]{}''."
                    "".format(self.new_bom_id.product_tmpl_id.default_code,
                              self.new_bom_id.product_tmpl_id.name),
            "view_type": "form",
            "view_mode": "tree",
            "views": [(view_id, "form")],
            "res_model": "mrp.eco",
            "view_id": view_id,
            "type": "ir.actions.act_window",
            "res_id": self.id,
            "target": "new",
        }

    def add_products(self):
        if self.mrp_bom_wizard_line:
            affected_part_line_list = []
            for line in self.mrp_bom_wizard_line:
                if line.selected_product:
                    affected_part_line_list.append(
                        (
                            0,
                            0,
                            {
                                "affected_product_id":
                                    line.affected_product_id.id
                            },
                        )
                    )

            if affected_part_line_list:
                self.affected_part_line = affected_part_line_list

    def select_all_products(self):
        if self.mrp_bom_wizard_line:
            for line in self.mrp_bom_wizard_line:
                if not line.is_product_available_in_eco:
                    line.selected_product = True

            self.add_products()
