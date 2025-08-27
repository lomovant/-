import hashlib

class User:
    """
    Базовий клас Користувача.

    Атрибути:
        username (str): Ім'я користувача.
        password_hash (str): Хеш пароля.
        is_active (bool): Вказує, чи активований обліковий запис.
    """
    def __init__(self, username, password, is_active=True):
        """
        Ініціалізує об'єкт Користувача.

        Args:
            username (str): Ім'я користувача.
            password (str): Пароль (буде захешований).
            is_active (bool, optional): Статус активації облікового запису. За замовчуванням True.
        """
        self.username = username
        # Хешування пароля для безпеки
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.is_active = is_active

    def verify_password(self, password):
        """
        Перевіряє введений пароль шляхом порівняння його хешу з збереженим хешем.

        Args:
            password (str): Пароль для перевірки.

        Returns:
            bool: True, якщо пароль правильний, інакше False.
        """
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def __str__(self):
        return f"Користувач: {self.username} (Активний: {self.is_active})"

class Administrator(User):
    """
    Клас Адміністратора, успадковує від User.

    Атрибути:
        permissions (list): Список дозволів адміністратора.
    """
    def __init__(self, username, password, is_active=True, permissions=None):
        """
        Ініціалізує об'єкт Адміністратора.

        Args:
            username (str): Ім'я користувача.
            password (str): Пароль.
            is_active (bool, optional): Статус активації. За замовчуванням True.
            permissions (list, optional): Список дозволів. За замовчуванням ['all'].
        """
        super().__init__(username, password, is_active)
        self.permissions = permissions if permissions is not None else ["all"] # Типовий дозвіл

    def grant_permission(self, permission):
        """
        Надає новий дозвіл адміністратору.
        """
        if permission not in self.permissions:
            self.permissions.append(permission)
            print(f"Дозвіл '{permission}' надано адміністратору {self.username}.")
        else:
            print(f"Адміністратор {self.username} вже має дозвіл '{permission}'.")

    def revoke_permission(self, permission):
        """
        Відкликає дозвіл у адміністратора.
        """
        if permission in self.permissions:
            self.permissions.remove(permission)
            print(f"Дозвіл '{permission}' відкликано у адміністратора {self.username}.")
        else:
            print(f"Адміністратор {self.username} не має дозволу '{permission}'.")

    def __str__(self):
        return f"Адміністратор: {self.username} (Активний: {self.is_active}, Дозволи: {self.permissions})"

class RegularUser(User):
    """
    Клас Звичайного користувача, успадковує від User.

    Атрибути:
        last_login_date (str): Дата останнього входу (може бути None).
    """
    def __init__(self, username, password, is_active=True, last_login_date=None):
        """
        Ініціалізує об'єкт Звичайного користувача.

        Args:
            username (str): Ім'я користувача.
            password (str): Пароль.
            is_active (bool, optional): Статус активації. За замовчуванням True.
            last_login_date (str, optional): Дата останнього входу. За замовчуванням None.
        """
        super().__init__(username, password, is_active)
        self.last_login_date = last_login_date

    def update_last_login(self, login_date):
        """
        Оновлює дату останнього входу.
        """
        self.last_login_date = login_date
        print(f"Дата останнього входу для {self.username} оновлена: {self.last_login_date}")

    def __str__(self):
        return (f"Звичайний користувач: {self.username} (Активний: {self.is_active}, "
                f"Останній вхід: {self.last_login_date if self.last_login_date else 'Ніколи'})")

class GuestUser(User):
    """
    Клас Гостя, успадковує від User. Має обмежені права.
    """
    def __init__(self, username="guest", password="guest_password"):
        """
        Ініціалізує об'єкт Гостя.

        Args:
            username (str, optional): Ім'я користувача. За замовчуванням "guest".
            password (str, optional): Пароль. За замовчуванням "guest_password".
        """
        # Гості зазвичай неактивні за замовчуванням або мають обмежений доступ
        super().__init__(username, password, is_active=False)
        self.access_level = "limited"

    def __str__(self):
        return (f"Гість: {self.username} (Активний: {self.is_active}, "
                f"Рівень доступу: {self.access_level})")

class AccessControl:
    """
    Клас Контролю доступу для управління користувачами.

    Атрибути:
        users (dict): Словник, де ключами є імена користувачів,
                      а значеннями - об'єкти класів користувачів.
    """
    def __init__(self):
        """
        Ініціалізує об'єкт Контролю доступу.
        """
        self.users = {}

    def add_user(self, user):
        """
        Додає нового користувача до системи.

        Args:
            user (User): Об'єкт користувача для додавання.

        Returns:
            bool: True, якщо користувача успішно додано, False, якщо користувач з таким ім'ям вже існує.
        """
        if user.username not in self.users:
            self.users[user.username] = user
            print(f"Користувача {user.username} ({type(user).__name__}) додано до системи.")
            return True
        else:
            print(f"Помилка: Користувач з ім'ям {user.username} вже існує.")
            return False

    def authenticate_user(self, username, password):
        """
        Перевіряє, чи існує користувач з таким ім'ям та чи правильний введений пароль.

        Args:
            username (str): Ім'я користувача для аутентифікації.
            password (str): Пароль для аутентифікації.

        Returns:
            User or None: Об'єкт користувача у разі успішної аутентифікації,
                          і None у разі невдачі (користувач не знайдений, неправильний пароль,
                          або обліковий запис неактивний).
        """
        user = self.users.get(username)
        if user:
            if not user.is_active:
                print(f"Аутентифікація не вдалась: Обліковий запис {username} неактивний.")
                return None
            if user.verify_password(password):
                print(f"Аутентифікація успішна для користувача {username}.")
                return user
            else:
                print(f"Аутентифікація не вдалась: Неправильний пароль для {username}.")
                return None
        else:
            print(f"Аутентифікація не вдалась: Користувача {username} не знайдено.")
            return None

# Приклад використання:
if __name__ == "__main__":
    # Створення системи контролю доступу
    access_system = AccessControl()

    # Створення різних типів користувачів
    admin1 = Administrator("admin_user", "securePa$$wOrd", permissions=["manage_users", "view_logs"])
    user1 = RegularUser("john_doe", "password123")
    user2 = RegularUser("jane_roe", "mysecret", is_active=False) # Неактивний користувач
    guest1 = GuestUser() # Використовує ім'я та пароль за замовчуванням

    # Додавання користувачів до системи
    access_system.add_user(admin1)
    access_system.add_user(user1)
    access_system.add_user(user2)
    access_system.add_user(guest1)
    access_system.add_user(RegularUser("john_doe", "another_pass")) # Спроба додати існуючого

    print("\n--- Тестування аутентифікації ---")
    # Успішна аутентифікація адміністратора
    authenticated_admin = access_system.authenticate_user("admin_user", "securePa$$wOrd")
    if authenticated_admin:
        print(f"Вітаємо, {authenticated_admin.username}! Ваш тип: {type(authenticated_admin).__name__}")
        if isinstance(authenticated_admin, Administrator):
            authenticated_admin.grant_permission("delete_data")
            print(f"Дозволи адміністратора: {authenticated_admin.permissions}")

    # Успішна аутентифікація звичайного користувача
    authenticated_user = access_system.authenticate_user("john_doe", "password123")
    if authenticated_user:
        print(f"Вітаємо, {authenticated_user.username}! Ваш тип: {type(authenticated_user).__name__}")
        if isinstance(authenticated_user, RegularUser):
            authenticated_user.update_last_login("2025-05-09 10:30:00")
            print(str(authenticated_user))

    # Невдала аутентифікація - неправильний пароль
    access_system.authenticate_user("john_doe", "wrongpassword")

    # Невдала аутентифікація - користувач не існує
    access_system.authenticate_user("unknown_user", "some_password")

    # Невдала аутентифікація - неактивний користувач
    access_system.authenticate_user("jane_roe", "mysecret")

    # Аутентифікація гостя (він неактивний за замовчуванням)
    authenticated_guest = access_system.authenticate_user("guest", "guest_password")
    if authenticated_guest: # Не пройде, бо is_active=False
         print(f"Вітаємо, {authenticated_guest.username}!")
    else:
        # Можна активувати гостя, якщо потрібно
        guest_obj = access_system.users.get("guest")
        if guest_obj:
            guest_obj.is_active = True
            print(f"\nОбліковий запис гостя '{guest_obj.username}' активовано.")
            authenticated_guest_active = access_system.authenticate_user("guest", "guest_password")
            if authenticated_guest_active:
                print(f"Вітаємо, {authenticated_guest_active.username}! Тип: {type(authenticated_guest_active).__name__}")
                print(str(authenticated_guest_active))


    print("\n--- Інформація про користувачів у системі ---")
    for username, user_obj in access_system.users.items():
        print(str(user_obj))
