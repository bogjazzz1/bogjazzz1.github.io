client_id = "747b8b77-661d-4bdd-b2be-8eb06c36badf"
secret = "93ce3aba-1f29-4783-bc22-d32838260a13"
auth = "NzQ3YjhiNzctNjYxZC00YmRkLWIyYmUtOGViMDZjMzZiYWRmOjkzY2UzYWJhLTFmMjktNDc4My1iYzIyLWQzMjgzODI2MGExMw=="

import requests
import uuid


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


'''response = get_token(auth)
if response != 1:
    print(response.text)
    giga_token = response.json()['access_token']
'''