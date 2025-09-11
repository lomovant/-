# Sales list
sales = [
    {"product": "apples", "quantity": 50, "price": 20},
    {"product": "bananas", "quantity": 30, "price": 25},
    {"product": "milk", "quantity": 40, "price": 30},
    {"product": "bread", "quantity": 60, "price": 15},
    {"product": "eggs", "quantity": 100, "price": 10},
    {"product": "oranges", "quantity": 20, "price": 50}
]


def calculate_revenue(sales_list):
    """Calculates total revenue for each product."""
    revenue_dict = {}

    for sale in sales_list:
        product = sale["product"]
        revenue = sale["quantity"] * sale["price"]

        if product in revenue_dict:
            revenue_dict[product] += revenue
        else:
            revenue_dict[product] = revenue

    return revenue_dict


# Calculate total revenue
revenue_dict = calculate_revenue(sales)

# List of products with revenue greater than 1000
high_revenue_products = [product for product, revenue in revenue_dict.items() if revenue > 1000]

# Output results
print("Total revenue by product:", revenue_dict)
print("Products with revenue greater than 1000:", high_revenue_products)
