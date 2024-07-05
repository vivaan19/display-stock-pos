/** @odoo-module **/

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";


patch(PaymentScreen.prototype, {

    async validateOrder(isForceValidate) {

        await super.validateOrder(...arguments);

        console.log("In Validate ---- ");

        try {
            
            var orders = this.pos.get_order().orderlines
            
            if (orders) {

                for (let i = 0; i < orders.length; i++) {

                    this.pos.db.get_product_by_id(orders[i].product.id).true_on_hand -= orders[i].quantity

                }
            }
        } 
        
        catch (error) {
            return;
            
        }

    }


});