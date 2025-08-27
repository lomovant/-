import json
import requests
import matplotlib.pyplot as plt

# URL для запиту
url = "https://bank.gov.ua/NBU_Exchange/exchange_site?start=20250317&end=20250321&valcode=eur&json"
response_data = requests.get(url)

# Перевірка статусу відповіді
if response_data.status_code != 200:
    print("Помилка отримання даних:", response_data.status_code)
    exit()

response_list = json.loads(response_data.content)

# Вивід отриманих даних для аналізу
print(json.dumps(response_list, indent=4, ensure_ascii=False))

exchange_date = []
exchange_rate = []

# Отримання курсів євро за попередній тиждень
for entry in response_list:
    if "exchangedate" in entry and "rate" in entry:
        date = entry["exchangedate"]
        rate = entry["rate"]
        print(f"{date}: {rate}")
        exchange_date.append(date)
        exchange_rate.append(rate)
    else:
        print("Помилка у форматі даних:", entry)

# Побудова графіка зміни курсу
plt.plot(exchange_date, exchange_rate, marker='o', linestyle='-')
plt.xlabel("Дата")
plt.ylabel("Курс EUR")
plt.title("Зміна курсу євро за тиждень")
plt.xticks(rotation=45)
plt.grid()
plt.show()

