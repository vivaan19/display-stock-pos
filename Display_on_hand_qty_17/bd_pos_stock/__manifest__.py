
# ver : odoo-17
{
    "name": "Display Location wise Stock in POS",
    "summary": """
        Show Product stock on POS Screen""",
    "description": """
        This Odoo app allows sellers to view and manage stock in the Point of Sale
        (POS) interface. They can choose to display "Quantity on Hand".
    """,
    
    "author": "Vivaan Shiromani",
    

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "point_of_sale",
    "version": "0.1",
    "license": "LGPL-3",
    # "price": "27.89",
    # "currency": "USD",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "point_of_sale",
        "stock",
    ],

    # always loaded
    "data": [
        "views/res_config_setting.xml",
    ],

    "assets": {
        "point_of_sale._assets_pos": [
            
            "bd_pos_stock/static/src/app/screens/product_screen/product_list/product_list.xml",
            
            "bd_pos_stock/static/src/overrides/models/models.js",
            
            "bd_pos_stock/static/src/overrides/models/pos_store.js",
            
            "bd_pos_stock/static/src/overrides/components/product_card/product_card.xml",
            
            "bd_pos_stock/static/src/overrides/components/product_card/product_card.js",
            
            "bd_pos_stock/static/src/app/screens/payment_screen/payment_screen.js",

            "bd_pos_stock/static/src/app/navbar/SyncStock/SyncStock.js",
            
            "bd_pos_stock/static/src/app/navbar/SyncStock/SyncStock.xml",

            "bd_pos_stock/static/src/overrides/components/navbar/navbar.js",
            
            "bd_pos_stock/static/src/overrides/components/navbar/navbar.xml",

        ],
    },
}
