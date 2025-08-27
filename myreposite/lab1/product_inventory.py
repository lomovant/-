# Початковий словник продуктів
inventory = {
    "яблука": 10,
    "банани": 3,
    "молоко": 7,
    "хліб": 2,
    "яйця": 12
}

def update_inventory(product, quantity):
    """Оновлює словник інвентарю, додаючи або віднімаючи кількість продукту."""
    if product in inventory:
        inventory[product] += quantity
        if inventory[product] < 0:
            inventory[product] = 0  # Запобігаємо від'ємним значенням
    else:
        if quantity > 0:
            inventory[product] = quantity  # Додаємо новий продукт

# Тестові операції
update_inventory("яблука", -4)  # Віднімаємо 4 яблука
update_inventory("хліб", 3)  # Додаємо 3 хліба
update_inventory("апельсини", 5)  # Додаємо новий продукт "апельсини"

# Список продуктів з кількістю менше ніж 5
low_stock_products = [product for product, count in inventory.items() if count < 5]

# Вивід результатів
print("Оновлений інвентар:", inventory)
print("Продукти, яких менше ніж 5:", low_stock_products)
