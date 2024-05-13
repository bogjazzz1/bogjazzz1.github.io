from flask import Flask, render_template, request, send_file
import os
from IT import replace_characters, get_chat_completion
from toren import get_token

app = Flask(__name__)

# Функция для замены персонажей и получения измененного текста
def process_file(text_file_path, character_a, character_b):
    # Получение токена для работы с GigaChat API
    auth_token = "NzQ3YjhiNzctNjYxZC00YmRkLWIyYmUtOGViMDZjMzZiYWRmOjkzY2UzYWJhLTFmMjktNDc4My1iYzIyLWQzMjgzODI2MGExMw=="
    response = get_token(auth_token)
    if response.status_code == 200:
        giga_token = response.json()['access_token']
    else:
        return "Ошибка при получении токена"

    # Выполнение замены персонажей в тексте
    text_file_path, character_a, character_b = map(str.strip, request.split())
    results = replace_characters(text_file_path, character_a, character_b)
    edited_text = ""
    for result in results:
        answer = get_chat_completion(giga_token, result)
        if answer.status_code == 200:
            edited_text += answer.json()['choices'][0]['message']['content']
        else:
            return "Ошибка при обработке текста"
    return edited_text

# Основная страница
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Получение файла с текстом и параметров персонажей
        text_file = request.files["text_file"]
        character_a = request.form["character_a"]
        character_b = request.form["character_b"]

        # Сохранение файла с текстом на сервере
        text_file_path = "uploads/" + text_file.filename
        text_file.save(text_file_path)

        # Обработка файла и получение измененного текста
        edited_text = process_file(text_file_path, character_a, character_b)
        if isinstance(edited_text, str):
            return edited_text
        else:
            # Сохранение измененного текста в файле
            output_file_path = "downloads/edited_text.txt"
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(edited_text)

            # Отправка файла пользователю для скачивания
            return send_file(output_file_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
