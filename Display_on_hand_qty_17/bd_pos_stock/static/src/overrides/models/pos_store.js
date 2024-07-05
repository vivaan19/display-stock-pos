/** @odoo-module */

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";


patch(PosStore.prototype, {

    // @Override
    async after_load_server_data(loadedData) {

        var res = await super.after_load_server_data(...arguments);

        console.log("pos config is show stock qty ---- ", this.config.is_show_stock_qty);

        var to_show_true_on_hand = this.config.is_show_stock_qty

        if (to_show_true_on_hand) {

            const reload_pos_data = await this.orm.call(

                "product.product",

                "get_reload_pos_data",

                [odoo.pos_session_id, this.config.id]
            );

            for (var [key, value] of Object.entries(reload_pos_data)) {

                // console.log("This db --- ", this.db);

                if (!this.db.product_by_id[key]) {

                    console.log("undef key product which are included in pos but dont have cate.--- ", key);

                }

                else {

                    this.db.product_by_id[key].true_on_hand = value;

                }

            }

        }

        return res

    },



    // async addProductFromUi(product, options) {

    //     var res = await super.addProductFromUi(...arguments);

    //     console.log("res ---- ", res);

    //     try {

    //         if (product.hasOwnProperty('true_on_hand')) {


    //             if (product.true_on_hand == 0) {

    //                 this.popup.add(ErrorPopup, {
    //                     title: "0 On-Hand Quantity Product",
    //                     body: (
    //                         "Product which have 0 on-hand Quantity cannot be added to current orders"
    //                     ),
    //                 });

    //                 this.get_order().removeOrderline(res)

    //             }
    //         }
    //     }

    //     catch (error) {

    //         console.log("In error ---- ", error);

    //         return;
    //     }

    //     return res;

    // }


    

    // async true_on_hand_zero(product) {

    //     this.notification = useService("notification");


    //     this.notification.add(
    //         _t("Cannot add 0 on-hand qty product"),
    //         {
    //             type: "danger",
    //         });


    //     console.log("In True on hand zero ------ ");

    // }





    // async addProductToCurrentOrder(product, options = {}) {

    //     console.log("Product 111 --- ", product);

    //     if (Number.isInteger(product)) {
    //         product = this.db.get_product_by_id(product);
    //         console.log("Prod ---- ", product);
    //     }
    //     this.get_order() || this.add_new_order();

    //     options = { ...options, ...(await product.getAddProductOptions()) };

    //     console.log("\n options ---- ", options);

    //     if (!Object.keys(options).length) {
    //         return;
    //     }

    //     try {

    //         if (product.hasOwnProperty('true_on_hand')) {

    //             if (product.true_on_hand == 0) {

    //                 this.popup.add(ErrorPopup, {
    //                     title: "0 On-Hand Quantity Product",
    //                     body: (
    //                         "Product which have 0 on-hand Quantity cannot be added to current orders"
    //                     ),
    //                 });

    //             }

    //             else {

    //                 // Add the product after having the extra information.
    //                 await this.addProductFromUi(product, options);
    //                 this.numberBuffer.reset();
    //             }

    //         }

    //         else {

    //             // Add the product after having the extra information.
    //             await this.addProductFromUi(product, options);
    //             this.numberBuffer.reset();

    //         }
    //     }
    //     catch (error) {

    //         console.log("Error in prod clicking --- ", error);

    //         return;
    //     }


    // }

    // async addProductToCurrentOrder(product, options = {}) {

    //     try {

    //         if (Number.isInteger(product)) {

    //             product = this.db.get_product_by_id(product);

    //         }

    //         if (product.hasOwnProperty('true_on_hand')) {

    //             if (product.true_on_hand == 0) {

    //                 this.popup.add(ErrorPopup, {
    //                     title: "0 On-Hand Quantity Product",
    //                     body: (
    //                         "Product which have 0 on-hand Quantity cannot be added to current orders"
    //                     ),
    //                 });


    //             }

    //         }

    //     }

    //     catch(error) {

    //         console.log("Error in prod clicking --- ", error);

    //         return;
    //     }

    //     var res = await super.addProductToCurrentOrder(...arguments);

    //     return res;

    // }

});