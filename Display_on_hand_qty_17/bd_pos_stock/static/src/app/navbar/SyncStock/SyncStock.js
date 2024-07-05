/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";


export class SyncStock extends Component {
    static template = "bd_pos_stock.SyncStock";

    setup() {

        this.pos = usePos();
        this.ui = useState(useService("ui"));

        this.orm = useService("orm");

        this.notification = useService("pos_notification");


    }

    async pos_stock_sync() {
        
        
        var given_config = new RegExp('[\?&]config_id=([^&#]*)').exec(window.location.href);
        this.config_id = given_config && given_config[1] && parseInt(given_config[1]) || false;

        console.log("config id  ---- ", this.config_id);

        var to_show_true_on_hand = this.pos.config.is_show_stock_qty

        console.log("Is show true on hand ----- ", to_show_true_on_hand);

        if (to_show_true_on_hand) {

            const reload_pos_data = await this.orm.call(
                
                "product.product",
                
                "get_reload_pos_data",
                
                [odoo.pos_session_id, this.config_id]
            );

            console.log("Reload pos data ----- ", reload_pos_data);

            for (var [key, value] of Object.entries(reload_pos_data)) {

                if (! this.pos.db.product_by_id[key]) {

                    console.log("undef key product which are included in pos but dont have cate.--- ", key);

                }

                else {

                    this.pos.db.product_by_id[key].true_on_hand = value;

                }
            
            }

            const current_cate = this.pos.selectedCategoryId

            console.log("Current cate ---- ", current_cate);

            this.pos.setSelectedCategoryId(null);
            this.pos.setSelectedCategoryId(current_cate);


            this.notification.add("Stock Quantity Updated", 500);



        }

    }
    
}