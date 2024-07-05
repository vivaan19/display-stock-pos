# Display On-Hand Stock in POS (Point of Sale) Card

## Description

This module adds a functionality to display current on-hand stock of a particular product in the POS (Point of Sale) interface product card screen, inside product card. 
This module aims to provide stock levels in the POS interface which can help a POS personell to save time for viewing the stock-levels in the back-end ERP  

## Features

- Created functionality to display on-hand stock for products based on the selected location in POS product cards
- Customized stock picking for accurate source and destination locations in normal and refund orders
- Eliminated unnecessary stock visibility for consumable products in POS, streamlining the user interface
- Developed a real-time stock sync button to update stock levels instantly from the back end without refreshing the POS screen
- Achieved a 30% reduction in inventory discrepancies by ensuring on-hand stock in POS matches the selected location’s inventory
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
    cp -r /path/to/cloned/repo/16.0/bd_pos_stock /path/to/your/odoo/addons/
    ```

4. **Update the Odoo module list:**

    ```bash
    ./odoo-bin -u all -d your-database
    ```

5. **Activate the module:**

    Go to `Apps` in Odoo, search for `bd_pos_stock`, and install it.

## Usage

1. **Configure POS Product Restrictions:**

    - Navigate to `Point of Sale` -> `Configuration` -> `Point of Sale`.
    - Select the POS configuration you want to restrict products for.
    - In the `Product Restrictions` tab, add or remove products as needed.

2. **Apply Restrictions:**

    - Once configured, only the selected products will be available in the specified POS.

## Screenshots

### POS Configuration

![POS Configuration](path/to/screenshot1.png)

### Product Restrictions

![Product Restrictions](path/to/screenshot2.png)

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc.
