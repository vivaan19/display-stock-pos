# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, RedirectWarning

from odoo.tools import float_is_zero, float_compare

from itertools import groupby
from collections import defaultdict

class BdPosOrder(models.Model):
    _inherit = "pos.order"

    def _create_order_picking(self):
        
        self.ensure_one()
        if self.shipping_date:
            self.sudo().lines._launch_stock_rule_from_pos_order_lines()
        else:
            if self._should_create_picking_real_time():
                picking_type = self.config_id.picking_type_id
                if self.partner_id.property_stock_customer:
                    destination_id = self.partner_id.property_stock_customer.id
                elif not picking_type or not picking_type.default_location_dest_id:
                    destination_id = self.env['stock.warehouse']._get_partner_locations()[0].id
                else:
                    destination_id = picking_type.default_location_dest_id.id

                pos_config_id = self.env["pos.session"].browse(self.session_id.id).config_id.id

                pickings = self.env['stock.picking']._create_picking_from_pos_order_lines(destination_id, self.lines, picking_type, self.partner_id, pos_config_id)
                pickings.write({'pos_session_id': self.session_id.id, 'pos_order_id': self.id, 'origin': self.name})

class BDStockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _create_picking_from_pos_order_lines(self, location_dest_id, lines, picking_type, partner=False, pos_config_id=False):
        """We'll create some picking based on order_lines"""

        pickings = self.env['stock.picking']
        stockable_lines = lines.filtered(lambda l: l.product_id.type in ['product', 'consu'] and not float_is_zero(l.qty, precision_rounding=l.product_id.uom_id.rounding))
        if not stockable_lines:
            return pickings
        positive_lines = stockable_lines.filtered(lambda l: l.qty > 0)
        negative_lines = stockable_lines - positive_lines

        if positive_lines:
            
            if not pos_config_id:
                location_id = picking_type.default_location_src_id.id
            
            else:
                
                custom_loc = self.env["pos.config"].sudo().browse(pos_config_id).stock_loc_ids.id
                
                if custom_loc:
                    location_id = custom_loc

                else:
                    location_id = picking_type.default_location_src_id.id



            positive_picking = self.env['stock.picking'].create(
                self._prepare_picking_vals(partner, picking_type, location_id, location_dest_id)
            )

            positive_picking._create_move_from_pos_order_lines(positive_lines)
            self.env.flush_all()
            try:
                with self.env.cr.savepoint():
                    positive_picking._action_done()
            except (UserError, ValidationError):
                pass

            pickings |= positive_picking
        
        
        if negative_lines:
            if picking_type.return_picking_type_id:
                return_picking_type = picking_type.return_picking_type_id
                return_location_id = return_picking_type.default_location_dest_id.id
            else:
                return_picking_type = picking_type
                return_location_id = picking_type.default_location_src_id.id

            
            temp_return_location_id = return_location_id

            if pos_config_id:
                
                location_dest_id = self.env['stock.location'].sudo().search([("usage", "=", "customer")], limit=1).id
                custom_loc = self.env["pos.config"].sudo().browse(pos_config_id).stock_loc_ids.id

                if custom_loc:
                    return_location_id = custom_loc
                    
                else:
                    return_location_id = temp_return_location_id     


            negative_picking = self.env['stock.picking'].create(
                self._prepare_picking_vals(partner, return_picking_type, location_dest_id, return_location_id)
            )
            negative_picking._create_move_from_pos_order_lines(negative_lines)
            self.env.flush_all()
            try:
                with self.env.cr.savepoint():
                    negative_picking._action_done()
            except (UserError, ValidationError):
                pass
            pickings |= negative_picking
        return pickings

class BdProductProduct(models.Model):

    _inherit = "product.product"

    true_on_hand = fields.Float("On hand based upon location selected", default="100.0")

    is_on_hand = fields.Boolean("Is qty on-hand")

    # main function which link js to py via orm call 
    def get_reload_pos_data(self, id):

        loc_to_update = self.env["pos.config"].sudo().browse(id).stock_loc_ids

        # details from stock.quant
        rec_quant_list = (
            self.env["stock.quant"]
            .sudo()
            .search(
                [
                    ("location_id.id", "=", loc_to_update.id),
                    ("product_id.available_in_pos", "=", True),
                ]
            )
        )

        prod_id_dic = {}

        for s_quant_id in rec_quant_list:

            s_prod_id = s_quant_id.product_id.id

            quantity = s_quant_id.inventory_quantity_auto_apply

            if s_prod_id in prod_id_dic:
                prod_id_dic[s_prod_id] += quantity

            else:
                prod_id_dic[s_prod_id] = quantity

        # print("\n Prod id ----- prev ----- ", prod_id_dic)

        prod_prod_all_rec = (
            self.env["product.product"].sudo().search([("available_in_pos", "=", True)])
        )

        # all prod ids
        all_prod_id_lst = prod_prod_all_rec.mapped("id")

        # excluded
        exec_prod_id_lst = list(set(all_prod_id_lst) - set(prod_id_dic.keys()))

        # exculded keys should have value to 0
        dictionary = {key: 0 for key in exec_prod_id_lst}

        prod_id_dic.update(dictionary)

        for prod_id in prod_id_dic:

            self.env["product.product"].sudo().browse(prod_id).write(
                {"true_on_hand": prod_id_dic[prod_id]}
            )

        print("\n Prod id dic ------ ", prod_id_dic)


        return prod_id_dic


    """
    # def find_prod_true_on_hand(self, id):

    #     print("\n id qty ... dict --- ", type(id))

    #     # settings = self.env["res.config.settings"].search([])

    #     loc_val_setting = self.env.user.current_stock_selected_id

    #     stock_quant_ids = self.env["stock.quant"].search(
    #         [("location_id.id", "=", loc_val_setting.id)]
    #     )

    #     print("\n stock qnat ids ---- ", stock_quant_ids)

    #     prod_dic = {}

    #     for pid in id:

    #         print("\n pid -- ", pid)

    #         for loc_id in stock_quant_ids:

    #             print("\n loc id prod id ---- ", loc_id.product_id.id)
    #             print("\n loc id prod name ---- ", loc_id.product_id.name)

    #             if loc_id.product_id.id == pid:

    #                 print("\n in ifff")

    #                 if pid in prod_dic:
    #                     prod_dic[pid] += loc_id.inventory_quantity_auto_apply

    #                 else:
    #                     prod_dic[pid] = loc_id.inventory_quantity_auto_apply
                    
    #                 print("\n prod dict ------- ", prod_dic)

    #     # for

    #     # prod_dic[pid] -= id[pid]

    #     print("\n prod _dic ---- ", prod_dic)

    #     return prod_dic
    """


# load field in pos in pos.session through loader method
class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):

        # load field to pos

        result = super()._loader_params_product_product()

        result["search_params"]["fields"].append("true_on_hand")
        result["search_params"]["fields"].append("is_on_hand")
        result["search_params"]["fields"].append("qty_available")
        result["search_params"]["fields"].append("detailed_type")

        return result


    def _get_pos_ui_pos_config(self, params):
        
        result = super(PosSession, self)._get_pos_ui_pos_config(params)

        is_show_stock_val = self.env["pos.config"].browse(result["id"]).is_show_stock_qty

        result["is_show_stock_qty"] = is_show_stock_val

        return result
    
class BdPosStock(models.Model):
    _inherit = "pos.config"

    is_show_stock_qty = fields.Boolean(
        string="Show Qty on Pos", default=False, store=True
    )

    def _get_default_location(self):
        return self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1).lot_stock_id


    stock_loc_ids = fields.Many2one(
        "stock.location", string="Select Location", store=True, default=_get_default_location
    )

    # Ignored field 
    qty_position_selection = fields.Selection(
        string="Position of Qty",
        selection=[("right", "Right"), ("left", "Left")],
        default="left",
        store=True,
    )

class bd_pos_stock(models.TransientModel):
    _inherit = "res.config.settings"

    pos_is_show_stock_qty = fields.Boolean(
        related="pos_config_id.is_show_stock_qty", readonly=False, store=True
    )

    pos_stock_loc_ids = fields.Many2one(
        related="pos_config_id.stock_loc_ids", readonly=False, store=True
    )

    # ignored field 
    qty_pos_setting = fields.Selection(
        related="pos_config_id.qty_position_selection", readonly=False, store=True
    )

    # @api.onchange('pos_picking_type_id')
    # def onchange_pos_picking_type_id(self):
        
    #     if self.pos_picking_type_id:
    #         self.pos_config_id.is_show_stock_qty = False
    

    @api.onchange('pos_is_show_stock_qty')
    def onchange_pos_is_show_stock_qty(self):
        
        if self.pos_is_show_stock_qty:
            self.pos_stock_loc_ids = self.env["stock.picking.type"].sudo().search([("id", "=", self.pos_config_id.picking_type_id.id)], limit=1).default_location_src_id.id
    
    @api.onchange('pos_stock_loc_ids')
    def onchange_pos_stock_loc_ids(self):

        if self.pos_stock_loc_ids.id:
        
            if self.pos_stock_loc_ids.id != self.env["stock.picking.type"].sudo().search([("id", "=", self.pos_config_id.picking_type_id.id)], limit=1).default_location_src_id.id:

                raise UserError(
                    _(
                        "Please select location same as Default location this POS's operation type"
                    )
                )
    
    # on save of res.config.settings
    @api.model
    def set_values(self):

        res = super(bd_pos_stock, self).set_values()

        # print("\n in set value --- op type", self.pos_picking_type_id.name)

        # print("\n in set value --- stock location before", self.pos_stock_loc_ids.name)

        self.pos_stock_loc_ids = self.pos_picking_type_id.default_location_src_id.id

        # print("\n in set value --- stock location after", self.pos_stock_loc_ids.name)


        # take always self.pos_config_id.<field_name>


        # here I have to set values for the field in product.product
        # as per data available for pos_stock_loc_ids
        
        is_qty = self.pos_config_id.is_show_stock_qty

        print("\n Is qty ==== ", is_qty)
        
        # if stock qty is false 

        if is_qty:

            if not self.pos_config_id.stock_loc_ids:
                raise UserError(
                    _(
                        "To use this functionality(Display Location wise Stock in POS), Please select at-least one location"
                    )
                )

            # # check if lot number group is enabled if yes then give validation error
            # if self.env.user.has_group("stock.group_production_lot"):
            #     raise UserError(
            #         _(
            #             "To use this functionality(Display Location wise Stock in POS), disable Lot/Serial Number, in settings"
            #         )
            #     )
            
            if self.pos_config_id.company_id.point_of_sale_update_stock_quantities == "closing":
                
                raise UserError(
                    _(
                        "To use this functionality(Display Location wise Stock in POS), enable Real-time inventory management in POS setting"
                    )
                )

        return res
