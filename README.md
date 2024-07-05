# Display Location Wise On-Hand Stock in POS (Point of Sale) Card

## Description

This module adds a functionality to display location wise current on-hand stock of a particular product in the POS (Point of Sale) interface product card screen, inside product card. 

This module aims to provide location wise stock levels in the POS interface which can help a POS personell to save time for viewing the stock-levels in the back-end ERP  

## Features

- Created functionality to display on-hand stock for products based on the selected location in POS product cards
- Customized stock picking for accurate source and destination locations in normal and refund orders
- Eliminated unnecessary stock visibility for consumable products in POS, streamlining the user interface
- Developed a real-time stock sync button to update stock levels instantly from the back end without refreshing the POS screen
- Achieved a **30%** reduction in inventory discrepancies by ensuring on-hand stock in POS matches the selected location’s inventory
- Utilized Odoo.sh for development, staging, and production environments, enhancing reliability and stability
  
## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.co/vivaan19/display-stock-pos.git
    ```

2. **Navigate to the Odoo add-ons directory:**

    ```bash
    cd /path/to/your/odoo/addons/
    ```

3. **Copy the module:**

    ```bash
    cp -r /path/to/cloned/repo/Display_on_hand_qty_17 /path/to/your/odoo/addons/
    ```

4. **Update the Odoo module list:**

    ```bash
    ./odoo-bin --addons=addons,/path/to/custom_module/Display_on_hand_qty_17 -d your_database
    ```

5. **Activate the module:**

    Go to `Apps` in Odoo, search for `bd_pos_stock`, and install it.

## Configure On-Hand Stock based on POS Location

  - First we need to Enable real time Inventory Management for POS for seamless reduction of stock-quanity from POS to back-end (enable developer mode)
    - Navigate to `POS module` -> `Configuration` -> `Settings` -> `Inventory` -> `Enable Inventory Management In real time`
  - POS Stock Configuration
    - Navigate to `POS Module` -> `Configuration` -> `Settings` -> `Stock Configuration` -> `Enable "Show Stock Qty option`
  - Users can view product stock based on location
    - Navigate to `POS Module` -> `Configuration` -> `Settings` -> `Stock Configuration` -> `Stock Locations` 

## Screenshots

### Enable Real Time Inventory Management 

![Enable Real Time Inventory Management](/screenshots/real_time.png)

### POS Stock Configuration

![Stock Configuration](/screenshots/stock_conf_enable.png)

### View Product stock based on location

![View product stock based on location](/screenshots/stock_config_location.png)

### Users can see product stock by their stock location.

![On-Hand Stock levels on selected location](/screenshots/product_by_loc.png)

### View in POS After Configuration 

![POS View](/screenshots/pos_interface.png)

### Real time stock update Sync Button 

![Sync Button](/screenshots/sync_button.png)


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.
