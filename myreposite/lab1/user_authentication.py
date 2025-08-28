import hashlib

# Початковий словник користувачів (логін, хешований пароль, ПІБ)
users = {
    "wulfiecs123": {
        "password": hashlib.md5("alex_under".encode()).hexdigest(),
        "full_name": "Lomov Anton"
    },
    "user456": {
        "password": hashlib.md5("petrenko".encode()).hexdigest(),
        "full_name": "Іван Петренко"
    }
}

def check_password(login, input_password):
    """Перевіряє введений пароль користувача."""
    if login in users:
        hashed_input = hashlib.md5(input_password.encode()).hexdigest()
        if hashed_input == users[login]["password"]:
            print(f"Вітаємо, {users[login]['full_name']}! Вхід виконано успішно.")
        else:
            print("Невірний пароль.")
    else:
        print("Користувача не знайдено.")

# Введення даних користувачем
login = input("Введіть логін: ")
password = input("Введіть пароль: ")

# Перевірка пароля
check_password(login, password)
