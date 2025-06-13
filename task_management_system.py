# Початковий словник задач
tasks = {
    "Написати звіт": "в процесі",
    "Перевірити пошту": "виконано",
    "Підготувати презентацію": "очікує",
    "Зателефонувати клієнту": "очікує",
    "Розробити план проекту": "в процесі"
}

def add_task(task_name, status="очікує"):
    """Додає нову задачу зі статусом (за замовчуванням 'очікує')."""
    if task_name not in tasks:
        tasks[task_name] = status
    else:
        print(f"Задача '{task_name}' вже існує.")

def remove_task(task_name):
    """Видаляє задачу, якщо вона існує."""
    if task_name in tasks:
        del tasks[task_name]
    else:
        print(f"Задача '{task_name}' не знайдена.")

def update_task_status(task_name, new_status):
    """Оновлює статус існуючої задачі."""
    if task_name in tasks:
        tasks[task_name] = new_status
    else:
        print(f"Задача '{task_name}' не знайдена.")

# Тестові операції
add_task("Купити канцелярію")  # Додаємо нову задачу
update_task_status("Написати звіт", "виконано")  # Оновлюємо статус
remove_task("Перевірити пошту")  # Видаляємо задачу

# Список задач зі статусом "очікує"
pending_tasks = [task for task, status in tasks.items() if status == "очікує"]

# Вивід результатів
print("Список задач:", tasks)
print("Задачі, що очікують виконання:", pending_tasks)
