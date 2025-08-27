import sqlite3
import hashlib

DB_NAME = 'user_accounts.db'

def setup_database():
    """Ініціалізує базу даних та таблицю користувачів, якщо вони не існують."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                username TEXT PRIMARY KEY,
                pass_hash TEXT NOT NULL,
                full_user_name TEXT NOT NULL
            )
        ''')
        conn.commit()

def _hash_password(password_text):
    """Хешує наданий пароль за допомогою SHA256."""
    return hashlib.sha256(password_text.encode()).hexdigest()

def register_new_user(uname, passwd, fullname):
    """Додає нового користувача до бази даних."""
    hashed_pass = _hash_password(passwd)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO credentials (username, pass_hash, full_user_name)
                VALUES (?, ?, ?)
            ''', (uname, hashed_pass, fullname))
            conn.commit()
            print(f"Користувача '{uname}' успішно зареєстровано.")
        except sqlite3.IntegrityError:
            print(f"Помилка: Користувач з логіном '{uname}' вже існує.")
        except Exception as e:
            print(f"Виникла помилка при додаванні користувача: {e}")


def modify_user_password(uname, new_passwd):
    """Оновлює пароль для існуючого користувача."""
    hashed_pass = _hash_password(new_passwd)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE credentials SET pass_hash = ?
            WHERE username = ?
        ''', (hashed_pass, uname))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Пароль для користувача '{uname}' оновлено.")
        else:
            print(f"Користувача '{uname}' не знайдено.")

def verify_user_credentials(uname, passwd_attempt):
    """Перевіряє, чи наданий пароль співпадає з хешем у базі даних."""
    hashed_attempt = _hash_password(passwd_attempt)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Використовуємо параметризований запит для безпеки
        cursor.execute('''
            SELECT pass_hash FROM credentials
            WHERE username = ?
        ''', (uname,))
        stored_data = cursor.fetchone()

    if stored_data:
        # stored_data[0] містить хеш пароля з бази даних
        return stored_data[0] == hashed_attempt
    return False

def display_menu():
    """Відображає головне меню програми."""
    print("\nМеню управління користувачами:")
    print("1. Зареєструвати нового користувача")
    print("2. Змінити пароль користувача")
    print("3. Увійти в систему (автентифікація)")
    print("4. Завершити роботу")

def run_application():
    """Головний цикл програми."""
    setup_database()

    while True:
        display_menu()
        user_choice = input("Ваш вибір: ")

        if user_choice == '1':
            login_val = input("Введіть бажаний логін: ")
            password_val = input("Введіть пароль: ")
            full_name_val = input("Введіть ваше повне ім'я (ПІБ): ")
            register_new_user(login_val, password_val, full_name_val)

        elif user_choice == '2':
            login_val = input("Введіть логін користувача, пароль якого потрібно змінити: ")
            new_password_val = input("Введіть новий пароль: ")
            modify_user_password(login_val, new_password_val)

        elif user_choice == '3':
            login_val = input("Введіть ваш логін: ")
            password_val = input("Введіть ваш пароль: ")
            if verify_user_credentials(login_val, password_val):
                print(" Вхід успішний! Ласкаво просимо.")
            else:
                print(" Неправильний логін або пароль.")

        elif user_choice == '4':
            print("Дякуємо за використання програми! ")
            break

        else:
            print(" Некоректний вибір. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    run_application()