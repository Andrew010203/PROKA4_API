import os
from dotenv import load_dotenv
import requests

load_dotenv()

# def get_token():
#     """Получение актуального Bearer токена"""
#     url = "https://aqa-proka4.org/sandbox/api/reset-token"
#
#     old_token = os.getenv('BEARER_TOKEN')
#
#     response = requests.post(url, headers={"Authorization": old_token})
#     new_token = response.json().get("bearer_token")
#
#     # Сохраняем с приставкой, чтобы Headers.base подхватил валидную строку
#     os.environ["NEW_TOKEN"] = f"Bearer {new_token}"
# get_token()


class Headers:

    base = {
        'Authorization': os.getenv("BEARER_TOKEN"),
        'Content-Type': 'application/json'
        }



