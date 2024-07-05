/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { useEnv, onMounted, onPatched, useComponent, useRef } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";


import { PosCollection } from "@point_of_sale/app/store/models";


// patch(PosCollection.prototype), {

//     add(item) {

//         console.log("Inheri ==== Item ------ ", item);
//         super.add(...arguments);

//     }
// }



// export class ProdClickOrder extends Order {

//     setup(_defaultObj, options) {

//         super.setup(...arguments);

//         this.popup = useService("popup");
//     }

//     async add_product(product, options) {

//         var res = await super.add_product(...arguments);

//         console.log("In add prod inheri ---- ");

//         return res;



//     }


// }


patch(Order.prototype, {

    // async add_product(product, options) {

    //     console.log("In inheri add product ----- ");

    //     try {

    //         if (product.true_on_hand == 0) {

    //             this.pos.env.services.popup.add(ErrorPopup, {
    //                 title: _t("0 On-Hand Quantity Product"),
    //                 body: _t("Product which have 0 on-hand Quantity cannot be added to current orders"),
    //             });

    //             return;

    //         }
    //     }

    //     catch (error) {

    //         console.log("Error when clicking ---- ", error);
    //         return;
    //     }

    //     var res = await super.add_product(...arguments);

    //     return res;

    // }

    add_orderline(line) {


        if (!line || !line.product) {
            return;
        }

        console.log("Inheri ---- add orderline --- ", line.product.true_on_hand);

        var prod_true_on_hand = line.product.true_on_hand

        var prod_type = line.product.detailed_type

        if (prod_true_on_hand == 0) {

            if (prod_type == "consu") {

                return super.add_orderline(...arguments);

            }

            else{

                this.pos.env.services.popup.add(ErrorPopup, {
                    title: _t("0 On-Hand Quantity Product"),
                    body: _t("Product which have 0 on-hand Quantity cannot be added to current orders"),
                });

            }

        }

        else {

            return super.add_orderline(...arguments);
        }


    }

})
