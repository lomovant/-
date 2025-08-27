import sqlite3
import datetime

# назва файлу нашої бази даних
DB_NAME = 'security_events.db'


def create_connection():
    """ підключаємось до SQLite і повертаємо об'єкт з'єднання """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        # дуже важиво для цілісності даних. вмикаємо зовнішні ключі
        conn.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(f"Ой, не вдалося підключитися до бази: {e}")
    return conn


def create_tables():
    """ створюємо таблички, якщо їх ще немає в базі """
    conn = create_connection()
    if not conn:
        print("Немає з'єднання, таблиці не створено.")
        return

    cursor = conn.cursor()
    try:
        # таблиця для джерел подій звідки приходять логи
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventSources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                location TEXT,
                type TEXT
            );
        """)

        # типи подій та їх серйозність
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventTypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT UNIQUE NOT NULL,
                severity TEXT
            );
        """)

        # основна таблиця, де зберігатимуться всі події безпеки
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SecurityEvents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                source_id INTEGER,
                event_type_id INTEGER,
                message TEXT,
                ip_address TEXT, -- може бути порожнім
                username TEXT,   -- теж може бути порожнім
                FOREIGN KEY (source_id) REFERENCES EventSources(id),
                FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
            );
        """)
        conn.commit()
        print("Структура таблиць готова.")
    except sqlite3.Error as e:
        print(f"Щось пішло не так при створенні таблиць: {e}")
    finally:
        if conn:
            conn.close()


def populate_initial_event_types():
    """ заповнюємо EventTypes початковим набором даних, щоб було з чим працювати """
    conn = create_connection()
    if not conn:
        return

    cursor = conn.cursor()
    # стандартні типи подій, які ми очікуємо бачити
    event_types_data = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]

    try:
        # insert or ignore щоб не було помилок, якщо запускаємо повторно
        cursor.executemany("INSERT OR IGNORE INTO EventTypes (type_name, severity) VALUES (?, ?)", event_types_data)
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Додано {cursor.rowcount} початкових типів подій.")
        else:
            print("Початкові типи подій вже були в базі.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні початкових типів подій: {e}")
    finally:
        if conn:
            conn.close()


def register_event_source(name, location, type_val):
    """ додаємо нове джерело подій наприклад новий сервер або фаєрвол """
    conn = create_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)",
                       (name, location, type_val))
        conn.commit()
        source_id = cursor.lastrowid
        print(f"Джерело '{name}' зареєстровано, ID: {source_id}.")
        return source_id
    except sqlite3.IntegrityError:  # це якщо ім'я вже зайняте
        print(f"Джерело '{name}' вже існує. Не додано.")
        cursor.execute("SELECT id FROM EventSources WHERE name = ?", (name,))
        existing_id_tuple = cursor.fetchone()
        # повернемо ID існуючого, якщо знайшли
        return existing_id_tuple[0] if existing_id_tuple else None
    except sqlite3.Error as e:
        print(f"Не вдалося зареєструвати джерело '{name}': {e}")
        return None
    finally:
        if conn:
            conn.close()


def register_event_type(type_name, severity):
    """ додаємо новий тип події, якщо такого ще немає """
    conn = create_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)",
                       (type_name, severity))
        conn.commit()
        type_id = cursor.lastrowid
        print(f"Тип події '{type_name}' зареєстровано, ID: {type_id}.")
        return type_id
    except sqlite3.IntegrityError:
        print(f"Тип події '{type_name}' вже існує. Не додано.")
        cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (type_name,))
        existing_id_tuple = cursor.fetchone()
        return existing_id_tuple[0] if existing_id_tuple else None
    except sqlite3.Error as e:
        print(f"Не вдалося зареєструвати тип події '{type_name}': {e}")
        return None
    finally:
        if conn:
            conn.close()


def log_security_event(source_id, event_type_id, message, ip_address=None, username=None):
    """ записуємо саму подію безпеки в базу. Час фіксується автоматично """
    conn = create_connection()
    if not conn:
        return None

    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (timestamp, source_id, event_type_id, message, ip_address, username))
        conn.commit()
        event_id = cursor.lastrowid
        # print(f"Подія безпеки ID: {event_id} записана.") # можна прибрати, щоб не було забагато виводу
        return event_id
    except sqlite3.Error as e:
        print(f"Помилка при записі події безпеки: {e}")
        return None
    finally:
        if conn:
            conn.close()


# --- далі йдуть функції для всяких запитів до бази ---

def get_failed_logins_last_24_hours():
    """ шукаємо всі невдалі спроби входу за останню добу """
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        # віднімаємо 24 години від поточного часу
        twenty_four_hours_ago = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            SELECT se.timestamp, es.name as source_name, se.ip_address, se.username, se.message
            FROM SecurityEvents se
            JOIN EventTypes et ON se.event_type_id = et.id
            JOIN EventSources es ON se.source_id = es.id
            WHERE et.type_name = 'Login Failed' AND se.timestamp >= ?
            ORDER BY se.timestamp DESC;
        """, (twenty_four_hours_ago,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Помилка при отриманні невдалих логінів: {e}")
        return []
    finally:
        if conn:
            conn.close()


def detect_potential_bruteforce_ips():
    """ спроба виявити IP, з яких хтось активно підбирає паролі, більше 5 невдалих спроб за годину """
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        one_hour_ago = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
        # шукаємо тип події Login Failed
        # потім групуємо по IP і рахуємо кількість таких подій за останню годину
        cursor.execute("""
            SELECT ip_address, COUNT(id) as failed_attempts, MIN(timestamp) as first_attempt, MAX(timestamp) as last_attempt
            FROM SecurityEvents
            WHERE event_type_id = (SELECT id FROM EventTypes WHERE type_name = 'Login Failed')
              AND timestamp >= ?
              AND ip_address IS NOT NULL
            GROUP BY ip_address
            HAVING COUNT(id) > 5 
            ORDER BY failed_attempts DESC;
        """, (one_hour_ago,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Помилка при детектуванні брутфорсу: {e}")
        return []
    finally:
        if conn:
            conn.close()


def get_aggregated_critical_events_by_source():
    """ витягуємо статистику по критичним подіям за останній тиждень, згруповану по джерелах """
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            SELECT es.name as source_name, 
                   COUNT(se.id) as event_count,
                   es.location, 
                   es.type as source_type 
            FROM SecurityEvents se
            JOIN EventTypes et ON se.event_type_id = et.id
            JOIN EventSources es ON se.source_id = es.id
            WHERE et.severity = 'Critical' AND se.timestamp >= ?
            GROUP BY es.name, es.location, es.type
            ORDER BY event_count DESC, es.name;
        """, (one_week_ago,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Помилка при отриманні агрегованих критичних подій: {e}")
        return []
    finally:
        if conn:
            conn.close()


def find_events_by_keyword(keyword):
    """ простий пошук подій, де в повідомленні є задане ключове слово """
    conn = create_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        # like '%слово%' шукає входження слова будь де в тексті
        cursor.execute(f"""
            SELECT se.timestamp, es.name as source_name, et.type_name as event_type,
                   se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventTypes et ON se.event_type_id = et.id
            JOIN EventSources es ON se.source_id = es.id
            WHERE se.message LIKE ?
            ORDER BY se.timestamp DESC;
        """, (f'%{keyword}%',))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Помилка при пошуку за ключовим словом '{keyword}': {e}")
        return []
    finally:
        if conn:
            conn.close()


def add_sample_data():
    """ додамо трохи даних для тестів, щоб база не була порожньою """
    print("\n--- Заповнення тестовими даними ---")

    src1_id = register_event_source("Firewall_Corp_HQ", "192.168.1.1", "Firewall")
    src2_id = register_event_source("WebServer_Prod_01", "10.0.0.5", "Web Server")
    src3_id = register_event_source("IDS_Sensor_DMZ", "172.16.0.10", "IDS")
    src4_id = register_event_source("Workstation_Admin", "192.168.1.100", "Workstation")

    login_s_id = get_event_type_id("Login Success")
    login_f_id = get_event_type_id("Login Failed")
    scan_id = get_event_type_id("Port Scan Detected")
    malware_id = get_event_type_id("Malware Alert")
    logout_id = register_event_type("User Logout", "Informational")

    if not all([src1_id, src2_id, src3_id, src4_id, login_s_id, login_f_id, scan_id, malware_id, logout_id]):
        print("Проблема з отриманням ID для тестових даних. Пропускаємо.")
        return

    print("\n--- Запис тестових подій ---")
    log_security_event(src1_id, login_f_id, "Невдалий логін admin", "101.102.103.104", "admin")
    log_security_event(src1_id, login_f_id, "Невдалий логін root", "101.102.103.104", "root")

    # імітуємо атаку перебору паролів
    for i in range(6):
        log_security_event(src2_id, login_f_id, f"Невдала спроба для testuser{i + 1}", "203.0.113.45",
                           f"testuser{i + 1}")

    log_security_event(src2_id, login_s_id, "Успішний вхід john.doe", "192.168.1.50", "john.doe")
    log_security_event(src3_id, scan_id, "Сканування портів з 45.55.65.75", "45.55.65.75")
    log_security_event(src1_id, malware_id, "Знайдено вірус Trojan.Generic на 192.168.1.200!", "192.168.1.200",
                       "system")
    log_security_event(src2_id, login_f_id, "Неправильний API ключ", "10.0.0.88")
    log_security_event(src4_id, logout_id, "jane.doe вийшла з системи.", "192.168.1.100", "jane.doe")
    log_security_event(src1_id, login_s_id, "VPN для guest_user", "99.88.77.66", "guest_user")
    log_security_event(src3_id, malware_id, "КРИТИЧНО: Шифрувальник Locky в атачменті у hr_dept", "172.16.0.20",
                       "hr_dept")

    # додамо пару старих подій, щоб перевірити фільтри по часу
    conn_temp = create_connection()
    if conn_temp:
        cursor_temp = conn_temp.cursor()
        two_days_ago = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")
        ten_days_ago = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
        try:
            if login_f_id and src1_id:  # перевірка чи ID дійсний
                cursor_temp.execute(
                    "INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username) VALUES (?, ?, ?, ?, ?, ?)",
                    (two_days_ago, src1_id, login_f_id, "Дуже старий невдалий логін", "1.2.3.4", "old_user"))
            if malware_id and src3_id:
                cursor_temp.execute(
                    "INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username) VALUES (?, ?, ?, ?, ?, ?)",
                    (ten_days_ago, src3_id, malware_id, "Архівний вірус знайдено", "10.10.10.10", "archivist"))
            conn_temp.commit()
            print("Додано пару старих подій для тестування фільтрів.")
        except sqlite3.Error as e:
            print(f"Помилка при додаванні старих тестових подій: {e}")
        finally:
            if conn_temp:
                conn_temp.close()
    print("Тестові дані додано.")


def get_event_type_id(type_name):
    """ маленька функція-помічник, щоб отримати ID типу події за його назвою """
    conn = create_connection()
    if not conn: return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (type_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Не вдалося знайти ID для типу '{type_name}': {e}")
        return None
    finally:
        if conn:
            conn.close()


def main():
    """ головна функція, яка все запускає """
    print("Система логування подій безпеки вітає вас!")

    create_tables()
    populate_initial_event_types()

    # перевіримо, чи є вже джерела. якщо немає, додамо тестові дані
    # це щоб не заповнювати базу однаковими даними кожен раз
    conn_check = create_connection()
    if conn_check:
        source_count = 0
        cursor_check = conn_check.cursor()
        try:
            cursor_check.execute("SELECT COUNT(id) FROM EventSources")
            source_count_tuple = cursor_check.fetchone()
            if source_count_tuple:
                source_count = source_count_tuple[0]
        except sqlite3.Error as e:
            print(f"Помилка при перевірці кількості джерел: {e}")
        finally:
            conn_check.close()

        if source_count == 0:
            print("Схоже, база порожня. Додамо трохи тестових даних.")
            add_sample_data()
        else:
            print(f"В базі вже є {source_count} джерел. Тестові дані не додаємо.")

    print("\n--- Демонстрація роботи з запитами ---")

    print("\n1. Шукаємо IP, з яких часто невдало логіняться можливий брутфорс:")
    potential_bruteforce = detect_potential_bruteforce_ips()
    if potential_bruteforce:
        for ip, count, first, last in potential_bruteforce:
            print(f"  IP: {ip}, спроб: {count} (з {first} по {last})")
    else:
        print("  Підозрілих IP не знайдено.")

    print("\n2. Невдалі спроби входу за останні 24 години:")
    recent_failed_logins = get_failed_logins_last_24_hours()
    if recent_failed_logins:
        for event_ts, src_name, ip_addr, usr, msg in recent_failed_logins:
            print(
                f"  - {event_ts} | Джерело: {src_name} | IP: {ip_addr or 'N/A'} | Користувач: {usr or 'N/A'} | Повідомлення: {msg}")
    else:
        print("  За останню добу невдалих логінів не було.")

    print("\n3. Критичні події за останній тиждень згруповані по джерелах:")
    critical_events_stats = get_aggregated_critical_events_by_source()
    if critical_events_stats:
        for src_name, count, loc, src_type in critical_events_stats:
            print(f"  Джерело: {src_name} (тип: {src_type}, місце: {loc or 'N/A'}) - Кількість критичних подій: {count}")
    else:
        print("  Критичних подій за тиждень немає. Все спокійно!")

    print("\n4. Шукаємо події, де згадується malware:")
    keyword_events_malware = find_events_by_keyword("malware")
    if keyword_events_malware:
        for ts, src, ev_type, msg, ip, user in keyword_events_malware:
            print(f"  - {ts} | {src} ({ev_type}) | IP: {ip or 'N/A'} | Користувач: {user or 'N/A'} | {msg}")
    else:
        print("  Слова malware в логах не знайдено.")

    print("\n5. Шукаємо події, де згадується admin:")
    keyword_events_admin = find_events_by_keyword("admin")
    if keyword_events_admin:
        for ts, src, ev_type, msg, ip, user in keyword_events_admin:
            print(f"  - {ts} | {src} ({ev_type}) | IP: {ip or 'N/A'} | Користувач: {user or 'N/A'} | {msg}")
    else:
        print("  Слова admin в логах не знайдено.")

    print("\n--- Спробуємо додати щось нове ---")
    new_src_id = register_event_source("Test_Router_X1", "192.168.0.254", "Router")
    new_type_id = register_event_type("Firmware Update", "Informational")

    if new_src_id and new_type_id:
        log_security_event(new_src_id, new_type_id, "Прошивка роутера оновлена до версії 2.5.1", "192.168.0.254",
                           "admin_local")
        print("Успішно додали тестове джерело, тип та подію.")

    print(f"\nРоботу завершено. База даних '{DB_NAME}' готова до аналізу.")


if __name__ == '__main__':
    main()