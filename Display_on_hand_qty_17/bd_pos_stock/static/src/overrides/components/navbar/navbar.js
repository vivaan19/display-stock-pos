/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";

import { SyncStock } from "../../../app/navbar/SyncStock/SyncStock";

patch(Navbar.prototype, {


    setup() {
        
        super.setup()

        // add SyncStock in static property called components
        Navbar.components.SyncStock = SyncStock;
    },
    

});

