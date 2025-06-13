def word_count(text):
    words = text.lower().split()
    word_dict = {}

    for word in words:
        word = word.strip(".,!?;:\"'()[]{}")  # Видаляємо знаки пунктуації
        if word:
            word_dict[word] = word_dict.get(word, 0) + 1

    return word_dict

# Тестовий рядок
text = "Сонце світило яскраво. Сонце зігрівало землю, сонце дарувало світло. Люди раділи, коли сонце з’являлося на небі. Воно було теплим, і кожен любив сонце. Вітер тихо гуляв між деревами. Вітер приносив свіжість, вітер грався листям. Інколи вітер ставав сильнішим, але вітер завжди був вільним."

# Отримання словника з підрахунком слів
word_dict = word_count(text)

# Список слів, які зустрічаються більше 3 разів
frequent_words = [word for word, count in word_dict.items() if count > 3]

# Виведення результатів
print("Словник частоти слів:", word_dict)
print("Слова, що зустрічаються більше 3 разів:", frequent_words)
