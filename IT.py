client_id = "747b8b77-661d-4bdd-b2be-8eb06c36badf"
secret = "93ce3aba-1f29-4783-bc22-d32838260a13"
auth = "NzQ3YjhiNzctNjYxZC00YmRkLWIyYmUtOGViMDZjMzZiYWRmOjkzY2UzYWJhLTFmMjktNDc4My1iYzIyLWQzMjgzODI2MGExMw=="

import os
import requests
import json
import uuid
import re

"""output_directory = "D:/sisisi"
output_file_name = "output_file.txt"
output_file_path = os.path.join(output_directory, output_file_name)
file_directory = "D:/sisisi"
file_name = "test.txt"
file_path = os.path.join(file_directory, file_name)
character_a = "Баба-Яга"
character_b = "Лёва"

"""
cluster_length = 4000
def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
    Выполняет POST-запрос к эндпоинту, который выдает токен.

    Параметры:
    - auth_token (str): токен авторизации, необходимый для запроса.
    - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

    Возвращает:
    - ответ API, где токен и срок его "годности".
    """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


response = get_token(auth)
if response != -1:
    token = response.json()['access_token']


def get_chat_completion(auth_token, user_message):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.

    Возвращает:
    - str: Ответ от API в виде текстовой строки.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",  # Используемая модель
        "messages": [
            {
                "role": "user",  # Роль отправителя (пользователь)
                "content": user_message  # Содержание сообщения
            }
        ],
        "temperature": 3,  # Температура генерации
        "top_p": 0.1,  # Параметр top_p для контроля разнообразия ответов
        "n": 1,  # Количество возвращаемых ответов
        "stream": False,  # Потоковая ли передача ответов
        "max_tokens": 4000,  # Максимальное количество токенов в ответе
        "repetition_penalty": 1,  # Штраф за повторения
        "update_interval": 1  # Интервал обновления (для потоковой передачи)
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',  # Тип содержимого - JSON
        'Accept': 'application/json',  # Принимаем ответ в формате JSON
        'Authorization': f'Bearer {auth_token}'  # Токен авторизации
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return -1


def replace_characters(file_path, character_a, character_b):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Вычисляем длину строки и вычитаем её из cluster_length
        max_cluster_length = cluster_length - len(
            f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n")

        clusters = []
        cluster_number = 1
        while len(text) > 0:
            if len(text) <= max_cluster_length:
                cluster_text = text[:max_cluster_length]
                text = text[max_cluster_length:]
            else:
                last_period_index = text[:max_cluster_length].rfind('.')
                cluster_text = text[:last_period_index + 1]
                text = text[last_period_index + 1:]

            cluster = f"Кластер {cluster_number}:\n"
            cluster += f"Замени в тексте ниже персонажа {character_a} на персонажа {character_b}.\n\n"
            cluster += cluster_text + '\n'
            clusters.append(cluster)
            cluster_number += 1

        return clusters

    except FileNotFoundError:
        return ["Указанный файл не найден."]


phrases_to_exclude = [r"Кластер \d"]
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    results = replace_characters(file_path, character_a, character_b)
    for result in results:
        answer = get_chat_completion(token, result)

        output_text = answer.json()['choices'][0]['message']['content']

        # Фильтруем вывод программы
        output_text = re.sub(r'Кластер \d+:', '', output_text)

        # Удаляем лишние пробелы в начале и конце строки
        output_text = output_text.strip()

        # Записываем отфильтрованный вывод программы в файл
        if output_text:  # Проверяем, что строка не пустая
            output_file.write(output_text + "\n")

        print(output_text)