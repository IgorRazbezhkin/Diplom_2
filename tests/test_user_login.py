import pytest
import allure
import urls
from helpers import login_user, get_json_response
from data import error_messages, keys, invalid_email, invalid_password


@allure.suite("Авторизация пользователя.")
class TestAuth:

    @allure.title("Успешная авторизация зарегистрированного пользователя.")
    @allure.description("Тест для проверки успешной авторизации зарегистрированного пользователя.")
    @allure.link(urls.api_documentation, name="API документация")

    def test_login_with_registered_user_success(self, registered_user):
        with allure.step("Отправить запрос на авторизацию существующего пользователя"):
            response = login_user(registered_user)
            response_json = get_json_response(response)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, (
                f"Ошибка при авторизации пользователя: статус {response.status_code}, "
                f"тело: {response.text}"
            )

        with allure.step("Проверить успешность запроса."):
            assert response_json.get(keys['success_key']) is True, (
                f"Авторизация пользователя не удалась: {response_json}"
            )

        with allure.step("Проверить наличие ключа 'accessToken'"):
            assert "accessToken" in response_json, (
                f"В ответе отсутствует accessToken. Тело: {response.text}"
            )

    @allure.title("Получение ошибки при авторизации пользователя с неверными email и паролем.")
    @allure.description("Тест для проверки получения ошибки при авторизации пользователя с неверными обязательными даннами.")
    @allure.link(urls.api_documentation, name="API документация")

    @pytest.mark.parametrize(
        "credentials_modifier, expected_message",
        [
            (lambda ud: {"email": invalid_email, "password": ud["password"]}, error_messages['incorrect_credentials']),
            (lambda ud: {"email": ud["email"], "password": invalid_password}, error_messages['incorrect_credentials']),
        ],
        ids=["invalid_email_correct_password", "correct_email_invalid_password"]
    )

    def test_login_invalid_credentials_error_received(self, registered_user, credentials_modifier, expected_message):
        with allure.step("Подготовить неверные учетные данные"):
            invalid_credentials = credentials_modifier(registered_user)

        with allure.step("Отправить запрос на логин"):
            response = login_user(invalid_credentials)
            response_json = get_json_response(response)

        with allure.step("Проверить код и сообщение об ошибке"):
            message = response_json.get(keys['message_key'])
            assert (response.status_code, message) == (401, expected_message)