import pytest
import requests
import allure
import urls
import helpers
from data import ERROR_MESSAGES, KEYS, UPDATED_PASSWORD, UPDATED_NAME


@allure.suite("Изменение данных пользователя.")
class TestUserDataUpdates:

    @allure.title("Успешное изменение данных для авторизованного пользователя")
    @allure.description("Проверка успешного изменения данных для авторизованного пользователя")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    @pytest.mark.parametrize(
        "field, value, check_login",
        [
            ("email", helpers.generate_random_email(), False),
            ("name", UPDATED_NAME, False),
            ("password", UPDATED_PASSWORD, True)
        ]
    )

    def test_authorized_updates_success(self, registered_user, auth_headers, field, value, check_login):
        with allure.step("Отправить запрос на обновление данных."):
            response = requests.patch(
                urls.ENDPOINTS['update_user'],
                headers=auth_headers,
                json={field: value}
            )
            response_json = response.json()

        with allure.step("Проверить статус ответа."):
            assert response.status_code == 200, (
                f"Ошибка при обновлении данных: статус {response.status_code}, тело: {response.text}"
            )

        with allure.step("Проверить успешность запроса."):
            assert response_json.get(KEYS['success_key']) is True, (
                f"Создание пользователя не удалось: {response_json}"
            )

        with allure.step("Проверить вход с обновленным паролем."):
            if check_login:
                login_response = requests.post(
                    urls.ENDPOINTS['login'],
                    json={"email": registered_user["email"], "password": value}
                )
                assert login_response.status_code == 200

    @allure.title("Получение ошибки при изменении данных для неавторизованного пользователя")
    @allure.description("Тест для проверки получение ошибки при изменении данных для неавторизованного пользователя")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    @pytest.mark.parametrize("field", ["email", "name", "password"])

    def test_unauthorized_updates_error_received(self, field):
        test_value = "test_value"  # Простое значение для теста

        with allure.step("Отправить запрос на обновление данных."):
            response = requests.patch(
                urls.ENDPOINTS['update_user'],
                json={field: test_value}
            )
            response_json = response.json()

        with allure.step("Проверить код и сообщение об ошибке"):
            message = response_json.get(KEYS['message_key'])
            assert (response.status_code, message) == (401, ERROR_MESSAGES['unauthorized_get_update']), (
                f"Ожидался статус 401 и сообщение '{ERROR_MESSAGES['unauthorized_get_update']}', "
                f"Получен статус {response.status_code} и сообщение '{message}'. Тело: {response.text}"
            )