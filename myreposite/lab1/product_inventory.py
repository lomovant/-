## -*- coding: utf-8 -*-

inventory = {
    "apples": 10,
    "bananas": 3,
    "milk": 7,
    "bread": 2,
    "eggs": 12
}

def update_inventory(product, quantity):
    """Update inventory by adding or subtracting product quantity."""
    if product in inventory:
        inventory[product] += quantity
        if inventory[product] < 0:
            inventory[product] = 0  # prevent negative values
    else:
        if quantity > 0:
            inventory[product] = quantity  # add new product

# Test operations
update_inventory("apples", -4)   # remove 4 apples
update_inventory("bread", 3)     # add 3 breads
update_inventory("oranges", 5)   # add new product "oranges"

# Products with quantity less than 5
low_stock_products = [product for product, count in inventory.items() if count < 5]

# Print results
print("Updated inventory:", inventory)
print("Products with less than 5 units:", low_stock_products)
