# Список продажів
sales = [
    {"продукт": "яблука", "кількість": 50, "ціна": 20},
    {"продукт": "банани", "кількість": 30, "ціна": 25},
    {"продукт": "молоко", "кількість": 40, "ціна": 30},
    {"продукт": "хліб", "кількість": 60, "ціна": 15},
    {"продукт": "яйця", "кількість": 100, "ціна": 10},
    {"продукт": "апельсини", "кількість": 20, "ціна": 50}
]


def calculate_revenue(sales_list):
    """Обчислює загальний дохід для кожного продукту."""
    revenue_dict = {}

    for sale in sales_list:
        product = sale["продукт"]
        revenue = sale["кількість"] * sale["ціна"]

        if product in revenue_dict:
            revenue_dict[product] += revenue
        else:
            revenue_dict[product] = revenue

    return revenue_dict


# Обчислення загального доходу
revenue_dict = calculate_revenue(sales)

# Список продуктів, що принесли дохід більше ніж 1000
high_revenue_products = [product for product, revenue in revenue_dict.items() if revenue > 1000]

# Вивід результатів
print("Загальний дохід по продуктах:", revenue_dict)
print("Продукти, що принесли дохід більше 1000:", high_revenue_products)
