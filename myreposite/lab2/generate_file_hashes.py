import hashlib

def generate_file_hashes(*file_paths):
    """
    Генерує SHA-256 хеші для вказаних файлів.

    Args:
        *file_paths (str): Змінна кількість шляхів до файлів.

    Returns:
        dict: Словник, де ключ - шлях до файлу, значення - SHA-256 хеш.
    """
    file_hashes = {}
    for file_path in file_paths:
        try:
            hasher = hashlib.sha256()
            # Відкриваємо файл у бінарному режимі 'rb' [cite: 6]
            with open(file_path, 'rb') as file:
                # Читаємо файл частинами (chunks) для ефективності з великими файлами
                while chunk := file.read(4096): # 4096 байт - типовий розмір блоку
                    hasher.update(chunk)
            # Отримуємо хеш у шістнадцятковому форматі [cite: 7]
            file_hashes[file_path] = hasher.hexdigest()
        except FileNotFoundError:
            print(f"Помилка: Файл '{file_path}' не знайдено.") # [cite: 8]
        except IOError as e:
            print(f"Помилка читання файлу '{file_path}': {e}") # [cite: 8]
        except Exception as e:
            print(f"Виникла неочікувана помилка під час обробки файлу '{file_path}': {e}")
    return file_hashes # [cite: 9]

# --- Приклад використання ---
# Використаємо файли
files_to_hash = ['non_existent_file.txt', 'apache_logs.txt']
hashes = generate_file_hashes(*files_to_hash)

print("\nSHA-256 хеші файлів:")
for file, file_hash in hashes.items():
    print(f"Файл: {file}\nХеш: {file_hash}\n")

# Приклад з файлом, якого не існує
hashes_with_error = generate_file_hashes('non_existent_file.txt', 'apache_logs.txt')
print("\nСпроба з неіснуючим файлом:")
for file, file_hash in hashes_with_error.items():
    print(f"Файл: {file}\nХеш: {file_hash}\n")
