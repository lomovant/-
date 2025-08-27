import re
from collections import Counter

def analyze_log_file(log_file_path):
    """
    Аналізує лог-файл HTTP-сервера для підрахунку кодів відповідей.

    Args:
        log_file_path (str): Шлях до лог-файлу.

    Returns:
        dict: Словник, де ключ - код відповіді, значення - кількість входжень.
              Повертає порожній словник у разі помилки.
    """
    status_code_counts = Counter()
    # Регулярний вираз для пошуку коду відповіді HTTP (перше число після запиту в лапках)
    # Приклад рядка: 83.149.9.216 - - [...] "GET ... HTTP/1.1" 200 203023 ...
    log_pattern = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD).*?" (\d{3}) ')

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = log_pattern.search(line)
                if match:
                    status_code = int(match.group(1))
                    status_code_counts[status_code] += 1
        return dict(status_code_counts)
    except FileNotFoundError:
        print(f"Помилка: Файл '{log_file_path}' не знайдено.")
        return {}
    except IOError as e:
        print(f"Помилка читання файлу '{log_file_path}': {e}")
        return {}
    except Exception as e:
        print(f"Виникла неочікувана помилка: {e}")
        return {}

# --- Приклад використання ---
log_file = 'apache_logs.txt' # Переконайся, що файл apache_logs.txt знаходиться в тій самій папці
results = analyze_log_file(log_file)

if results:
    print("\nРезультати аналізу лог-файлу:")
    # Сортування за кодом відповіді для кращого вигляду
    for code in sorted(results.keys()):
      print(f"Код {code}: {results[code]} разів")
