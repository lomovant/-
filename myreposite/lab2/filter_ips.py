from collections import Counter
import re

def filter_ips(input_file_path, output_file_path, allowed_ips):
    """
    Фільтрує IP-адреси з лог-файлу за списком дозволених
    та записує кількість їх входжень у вихідний файл.

    Args:
        input_file_path (str): Шлях до вхідного лог-файлу.
        output_file_path (str): Шлях до вихідного файлу з результатами.
        allowed_ips (list): Список рядків з дозволеними IP-адресами.
    """
    allowed_ip_counts = Counter()
    # Регулярний вираз для вилучення IP-адреси на початку рядка
    ip_pattern = re.compile(r"^([\d\.]+)\s")

    try:
        # Читаємо вхідний файл [cite: 10]
        with open(input_file_path, 'r', encoding='utf-8') as infile:
            for line in infile:
                match = ip_pattern.match(line)
                if match:
                    ip_address = match.group(1)
                    # Перевіряємо, чи IP є в списку дозволених [cite: 11]
                    if ip_address in allowed_ips:
                        allowed_ip_counts[ip_address] += 1 # [cite: 12]

        # Записуємо результати у вихідний файл [cite: 13]
        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            if not allowed_ip_counts:
                outfile.write("Дозволені IP-адреси не знайдено у лог-файлі.\n")
            else:
                outfile.write("Статистика входжень дозволених IP-адрес:\n")
                # Сортуємо для кращого вигляду
                for ip in sorted(allowed_ip_counts.keys()):
                    outfile.write(f"{ip} - {allowed_ip_counts[ip]}\n") # [cite: 13]
        print(f"Результати фільтрації IP-адрес записано у файл '{output_file_path}'")

    except FileNotFoundError:
        print(f"Помилка: Вхідний файл '{input_file_path}' не знайдено.") # [cite: 14]
    except IOError as e:
        print(f"Помилка вводу/виводу під час роботи з файлами: {e}") # [cite: 14]
    except Exception as e:
        print(f"Виникла неочікувана помилка: {e}")

# --- Приклад використання ---
input_log = 'apache_logs.txt'
output_results = 'filtered_ips.txt'
# Задаємо список дозволених IP-адрес [cite: 12]
# (Візьмемо кілька IP з наданого лог-файлу apache_logs.txt [cite: 1500, 1508, 1509] для прикладу)
allowed_ips_list = ['83.149.9.216', '66.249.73.135', '110.136.166.128', '192.0.2.1'] # Додамо один IP, якого немає в логах

filter_ips(input_log, output_results, allowed_ips_list)
