import pytest
import random
import string
import requests
import urls


def generate_random_email(length=8):
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"user_{random_chars}@yandex.ru"

def register_user(user_data):
    response = requests.post(urls.endpoints['register'], json=user_data)
    return response

def login_user(user_data):
    response = requests.post(urls.endpoints['login'], json=user_data)
    return response

def get_json_response(response):
    try:
        return response.json()
    except ValueError:
        pytest.fail(f"Ответ не является JSON: {response.text}")
    return None