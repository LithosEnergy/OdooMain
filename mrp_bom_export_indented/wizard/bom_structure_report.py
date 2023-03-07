# -*- coding: utf-8 -*-
from odoo import models, fields

# import StringIO
import io
from xlwt import XFStyle, Alignment
import xlwt
import base64


class BomStructureReportWizard(models.TransientModel):
    _name = "bom.structure.report.wizard"

    state = fields.Selection(
        [("draft", "Draft"), ("done", "Done")], "State", default="draft"
    )
    file_name = fields.Char("File Name", default="BomStructure")
    data = fields.Binary("Report File")

    # Calculates the width of the column
    def get_width(self, num_characters):
        return int((1 + num_characters) * 256)

    def print_bom_children(
        self, ch, sheet1, row, level, col2, col3, qty=1.0, uom=False
    ):
        # style1 = XFStyle()
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        style_center = XFStyle()
        style_center.alignment = al
        i, j = row, level
        j += 1
        price = 0.0
        route_ids = ""
        for seller in ch.product_id.seller_ids:
            price = seller.price or 0.0
        if (
            ch.product_id
            and ch.product_id.default_code
            and len(ch.product_id.default_code) > col2
        ):
            col2 = len(ch.product_id.default_code)
        if (
            ch.product_id
            and ch.product_id.name
            and len(ch.product_id.name) > col3
        ):
            col3 = len(ch.product_id.name)

        count = 0
        if ch.product_id.seller_ids:
            for seller in ch.product_id.seller_ids:
                count += 1
        if ch.product_id.route_ids:
            route_count = len(ch.product_id.route_ids)
            rc = 0
            for route in ch.product_id.route_ids:
                route_ids += str(route.name)
                rc += 1
                if route_count != rc:
                    route_ids += ","

        qty_per_bom = ch.bom_id.product_qty
        if uom:
            if uom != ch.bom_id.product_uom_id:
                qty = uom._compute_quantity(qty, ch.bom_id.product_uom_id)
            pqty = (ch.product_qty * qty) / qty_per_bom
        else:
            # for the first case, the ponderation is right
            pqty = ch.product_qty * qty
        puom = ch.product_uom_id
        try:
            sheet1.write(i, 1, "> " * j)
        except:
            i += 1
            sheet1.write(i, 1, "> " * j)
        operation_ids = ""
        bom_type = ""
        for product_bom in ch.product_id.bom_ids:
            if product_bom.operation_ids:
                operation_ids = [
                    workcenter.name
                    for workcenter in product_bom.operation_ids.workcenter_id
                ]
            if product_bom.type:
                bom_type = (
                    dict(product_bom._fields["type"].selection).get(
                        product_bom.type
                    )
                    or ""
                )
        sheet1.write(i, 2, str(ch.product_id.default_code or ""), style_center)
        sheet1.write(i, 3, str(ch.product_id.display_name or ""))
        sheet1.write(
            i,
            4,
            str(
                dict(
                    ch.product_id.product_tmpl_id._fields["type"].selection
                ).get(ch.product_id.product_tmpl_id.type)
                or ""
            ),
        )
        sheet1.write(i, 5, route_ids or "")
        sheet1.write(i, 6, str(price), style_center)
        sheet1.write(i, 7, str(ch.product_id.weight or 0.0), style_center)
        sheet1.write(i, 8, str(pqty), style_center)
        sheet1.write(i, 9, str(ch.product_uom_id.name or ""), style_center)
        sheet1.write(i, 10, str(ch.bom_id.code or ""), style_center)
        sheet1.write(i, 11, str(bom_type), style_center)
        sheet1.write(i, 12, str(operation_ids), style_center)
        if ch.product_id.seller_ids:
            for seller in ch.product_id.seller_ids:
                # sheet1.write(i, 13, '>',style_center)
                sheet1.write(i, 13, str(seller.name.name or ""), style_center)
                sheet1.write(
                    i, 14, str(seller.product_code or ""), style_center
                )
                sheet1.write(i, 15, str(seller.min_qty or ""), style_center)
                sheet1.write(i, 16, str(seller.delay or ""), style_center)
                i += 1

        if ch.child_bom_id and ch.child_bom_id.bom_line_ids.ids:
            i += 1
            for child in ch.child_line_ids:
                i = self.print_bom_children(
                    child, sheet1, i, j, col2, col3, pqty, puom
                )
        j -= 1
        return i

    def get_print_report(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        bom_ids = self.env["mrp.bom"].browse(active_ids)
        al = Alignment()
        al.horz = Alignment.HORZ_CENTER
        al.vert = Alignment.VERT_CENTER
        style1 = XFStyle()
        style2 = XFStyle()
        style_center = XFStyle()
        style_center.alignment = al
        style2.alignment = al
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Sheet 1")
        sheet1.write(0, 0, "BOM Name", style1)
        sheet1.write(0, 1, "Level", style2)
        sheet1.write(0, 2, "Product Reference", style1)
        sheet1.write(0, 3, "Product Name", style1)
        sheet1.write(0, 4, "Product Type", style1)
        sheet1.write(0, 5, "Route", style1)
        sheet1.write(0, 6, "Product price", style2)
        sheet1.write(0, 7, "Product weight", style2)
        sheet1.write(0, 8, "Quantity", style2)
        sheet1.write(0, 9, "Unit of Measure", style1)
        sheet1.write(0, 10, "Reference", style1)
        sheet1.write(0, 11, "Bom Type", style2)
        sheet1.write(0, 12, "Routing", style2)
        # sheet1.write(0, 13, 'Vendor Level',style2)
        sheet1.write(0, 13, "Supplier", style2)
        sheet1.write(0, 14, "Vendor Product Code", style2)
        sheet1.write(0, 15, "Quantity", style2)
        sheet1.write(0, 16, "Delivery Lead Time", style2)
        col0 = 30
        col2 = 20
        col3 = 30
        i = 1
        for o in bom_ids:
            price = 0.0
            route_ids = ""
            for seller in o.product_tmpl_id.seller_ids:
                price = seller.price or 0.0
            if len(o.product_tmpl_id.name) > col0:
                col0 = len(o.product_tmpl_id.name)
            if (
                o.product_id
                and o.product_id.default_code
                and len(o.product_id.default_code) > col2
            ):
                col2 = len(o.product_id.default_code)
            if (
                o.product_id
                and o.product_id.name
                and len(o.product_id.name) > col3
            ):
                col3 = len(o.product_id.name)
            if o.product_id.route_ids:
                route_count = len(o.product_id.route_ids)
                rc = 0
                for route in o.product_id.route_ids:
                    route_ids += str(route.name)
                    rc += 1
                    if route_count != rc:
                        route_ids += ","
            elif o.product_tmpl_id.route_ids:
                route_count = len(o.product_tmpl_id.route_ids)
                rc = 0
                for route in o.product_tmpl_id.route_ids:
                    route_ids += str(route.name)
                    rc += 1
                    if route_count != rc:
                        route_ids += ","
            sheet1.write(i, 0, str(o.product_tmpl_id.name or ""), style1)
            sheet1.write(i, 1, str(""), style_center)
            sheet1.write(
                i, 2, str(o.product_tmpl_id.default_code or ""), style_center
            )
            sheet1.write(i, 3, str(o.product_tmpl_id.name or ""), style1)
            sheet1.write(
                i,
                4,
                str(
                    dict(o.product_tmpl_id._fields["type"].selection).get(
                        o.product_tmpl_id.type
                    )
                    or ""
                ),
                style1,
            )  # ********************************
            sheet1.write(i, 5, route_ids or "")
            sheet1.write(i, 6, str(price), style_center)
            sheet1.write(
                i, 7, str(o.product_tmpl_id.weight or 0.0), style_center
            )
            sheet1.write(i, 8, str(o.product_qty or 0), style_center)
            sheet1.write(i, 9, str(o.product_uom_id.name or ""), style_center)
            sheet1.write(i, 10, str(o.code or ""), style_center)
            sheet1.write(
                i,
                11,
                str(dict(o._fields["type"].selection).get(o.type) or ""),
                style_center,
            )  # ***************************
            sheet1.write(
                i,
                12,
                str(
                    [
                        workcenter.name
                        for workcenter in o.operation_ids.workcenter_id
                    ]
                    or ""
                ),
                style_center,
            )
            if o.product_tmpl_id.seller_ids:
                for seller in o.product_tmpl_id.seller_ids:
                    # sheet1.write(i, 13, '>',style_center)
                    sheet1.write(
                        i, 13, str(seller.name.name or ""), style_center
                    )
                    sheet1.write(
                        i, 14, str(seller.product_code or ""), style_center
                    )
                    sheet1.write(
                        i, 15, str(seller.min_qty or ""), style_center
                    )
                    sheet1.write(i, 16, str(seller.delay or ""), style_center)
                    i += 1
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_bom_children(ch, sheet1, i, j, col2, col3)
        sheet1.col(0).width = self.get_width(col0)
        sheet1.col(1).width = self.get_width(6)
        sheet1.col(2).width = self.get_width(col2)
        sheet1.col(3).width = self.get_width(col3)
        sheet1.col(4).width = self.get_width(15)
        sheet1.col(5).width = self.get_width(30)
        sheet1.col(6).width = self.get_width(15)
        sheet1.col(7).width = self.get_width(16)
        sheet1.col(8).width = self.get_width(15)
        sheet1.col(9).width = self.get_width(20)
        sheet1.col(12).width = self.get_width(20)
        # sheet1.col(13).width = self.get_width(20)
        sheet1.col(11).width = self.get_width(30)
        sheet1.col(14).width = self.get_width(25)
        sheet1.col(13).width = self.get_width(25)
        sheet1.col(16).width = self.get_width(25)

        file_name = self.file_name
        if ".xls" not in file_name:
            file_name = file_name + ".xls"
        fp = io.BytesIO()
        book.save(fp)
        fp.seek(0)
        self.data = base64.encodebytes(fp.read())
        self.file_name = file_name
        self.state = "done"
        fp.close()
        return {
            "type": "ir.actions.act_window",
            "res_model": "bom.structure.report.wizard",
            "view_mode": "form",
            # 'view_type': 'form',
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }
