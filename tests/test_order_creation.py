import pytest
import requests
import allure
import urls
import helpers
from data import error_messages, keys


@allure.suite("Создание заказа.")
class TestOrderCreation:

    @allure.title("Успешное создание заказа авторизованного и неавторизованного пользователя с ингредиентами в запросе.")
    @allure.description("Тест для проверки успешного создания заказа авторизованного и неавторизованного пользователя с ингредиентами в запросе.")
    @allure.link(urls.api_documentation, name="API документация")

    @pytest.mark.parametrize(
        "headers_provider, test_id",
        [
            (lambda h: h, "auth_with_ingredients"),
            (lambda _: {}, "no_auth_with_ingredients")
        ]
    )

    def test_create_order_with_ingredients_success(self, auth_headers, order_payload, headers_provider, test_id):
        with allure.step("Отправить запрос на создание заказа с ингредиентами."):
            response = requests.post(
                urls.endpoints['create_order'],
                headers=headers_provider(auth_headers),
                json=order_payload
            )
            response_data = helpers.get_json_response(response)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, (
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверить успешность запроса."):
            assert response_data[keys['success_key']] is True, (
                f"Ожидалось success=True, получено {response_data[keys['success_key']]}. "
                f"Тело: {response_data}"
            )

        with allure.step("Проверить наличие ключей 'name' и 'order' в ответе"):
            assert keys['name_key'] in response_data, "В ответе отсутствует поле 'name'"
            assert keys['order_key'] in response_data, "В ответе отсутствует поле 'order'"

    @allure.title("Получение ошибки при создании заказа авторизованного и неавторизованного пользователя без ингредиентов в запросе.")
    @allure.description("Тест для проверки получения ошибки при создании заказа авторизованного и неавторизованного пользователя без ингредиентов в запросе.")
    @allure.link(urls.api_documentation, name="API документация")

    @pytest.mark.parametrize(
        "headers_provider, test_id",
        [
            (lambda h: h, "auth_without_ingredients"),
            (lambda _: {}, "no_auth_without_ingredients")
        ]
    )

    def test_create_order_without_ingredients_error_received(self, auth_headers, order_payload, headers_provider, test_id):
        with allure.step("Отправить запрос на создание заказа с пустым списком ингредиентов."):
            response = requests.post(
                urls.endpoints['create_order'],
                headers=headers_provider(auth_headers),
                json={"ingredients": []}
            )
            response_data = helpers.get_json_response(response)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 400, (
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверить неуспешность запроса"):
            assert response_data[keys['success_key']] is False, (
                f"Ожидалось success=False, получено {response_data[keys['success_key']]}. "
                f"Тело: {response_data}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            assert response_data[keys['message_key']] == error_messages['no_ingredients_provided'], (
                f"Ожидалось сообщение '{error_messages['no_ingredients_provided']}', "
                f"получено '{response_data[keys['message_key']]}'"
            )

    @allure.title("Получение ошибки при создании заказа авторизованного и неавторизованного пользователя с неправильными хешами ингредиентов в запросе.")
    @allure.description("Тест для проверки получения ошибки при создании заказа авторизованного и неавторизованного пользователя с неправильными хешами ингредиентов в запросе.")
    @allure.link(urls.api_documentation, name="API документация")

    @pytest.mark.parametrize(
        "headers_provider, invalid_hashes, expected_status, test_id",
        [
            (lambda h: h, ["invalid_hash"], 400, "auth_invalid_hash"),
            (lambda _: {}, ["invalid_hash_1", "invalid_hash_2"], 500, "no_auth_invalid_hashes")
        ]
    )

    def test_create_order_with_invalid_hashes_error_received(
        self, auth_headers, headers_provider, invalid_hashes, expected_status, test_id
    ):
        with allure.step("Отправить запрос на создание заказа с неправильными хешами ингредиентов."):
            response = requests.post(
                urls.endpoints['create_order'],
                headers=headers_provider(auth_headers),
                json={"ingredients": invalid_hashes}
            )

        with allure.step("Проверить статус ответа"):
            assert response.status_code == expected_status, (
                f"Ожидался статус {expected_status}, получен {response.status_code}. "
                f"Тело: {response.text}"
            )