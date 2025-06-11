import pytest
import requests
import urls
import helpers
from data import PASSWORD, NAME


@pytest.fixture
def unique_user():
    return {
        "email": helpers.generate_random_email(),
        "password": PASSWORD,
        "name": NAME
    }


@pytest.fixture
def registered_user(unique_user):
    response = helpers.register_user(unique_user)
    assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
    return unique_user


@pytest.fixture
def auth_token(registered_user):
    login_response = helpers.login_user(registered_user)
    assert login_response.status_code == 200

    token = login_response.json().get("accessToken")
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    return token


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture(scope="function")
def create_and_delete_user():
    user_data = {
        "email": helpers.generate_random_email(),
        "password": PASSWORD,
        "name": NAME
    }

    response = helpers.register_user(user_data)
    assert response.status_code == 200

    yield user_data

    login_response = helpers.login_user(user_data)
    assert login_response.status_code == 200

    token = login_response.json()["accessToken"].split(" ")[1]
    headers = {"authorization": f"Bearer {token}"}
    delete_response = requests.delete(urls.ENDPOINTS['delete_user'], headers=headers)
    assert delete_response.status_code in [200, 202]


@pytest.fixture
def ingredients():
    response = requests.get(urls.ENDPOINTS['get_ingredients'])
    assert response.status_code == 200
    return response.json()['data']


@pytest.fixture
def order_payload(ingredients):
    return {'ingredients': [ingredients[0]['_id'], ingredients[1]['_id']]}