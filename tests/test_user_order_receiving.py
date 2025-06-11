import pytest
import requests
import allure
import urls
from data import ERROR_MESSAGES, KEYS


@allure.suite("Получение заказа пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказа авторизованным пользователем.")
    @allure.description("Тест для проверки успешного получение заказа авторизованным пользователем.")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    @pytest.mark.usefixtures("create_and_delete_user")

    def test_get_user_orders_authorized_success(self, auth_headers, order_payload):
        with allure.step("Отправить запрос на создание заказа авторизованным пользователем."):
            create_order_response = requests.post(
                urls.ENDPOINTS['create_order'],
                headers=auth_headers,
                json=order_payload
            )
            assert create_order_response.status_code == 200, (
                f"Не удалось создать заказ. статус: {create_order_response.status_code}, "
                f"тело: {create_order_response.text}"
            )

        with allure.step("Отправить запрос на получение заказа авторизованным пользователем."):
            get_orders_response = requests.get(
                urls.ENDPOINTS['get_user_orders'],
                headers=auth_headers
            )
            response_json = get_orders_response.json()

        with allure.step("Проверить статус ответа."):
            assert get_orders_response.status_code == 200, (
                f"Не удалось получить заказ, статус: {get_orders_response.status_code}, "
                f"тело: {get_orders_response.text}"
            )

        with allure.step("Проверить успешность запроса."):
            assert response_json.get(KEYS['success_key']) is True, (
                f"Получить заказ не удалось: {response_json}"
            )

        with allure.step("Проверить наличие ключа 'orders' в ответе."):
            assert KEYS['orders_key'] in response_json, (
                f"Отсутствует ключ {KEYS['orders_key']} в ответе"
            )

        with allure.step("Проверить, что ответ не пустой список."):
            assert isinstance(response_json[KEYS['orders_key']], list), "Заказы должны быть списком"
            assert len(response_json[KEYS['orders_key']]) > 0, "Список заказов пуст"

        with allure.step("Проверить наличие ключей 'number_key' и 'status_key' в ответе."):
            first_order = response_json[KEYS['orders_key']][0]
            assert KEYS['number_key'] in first_order, f"Отсутствует ключ {KEYS['number_key']} в заказе"
            assert KEYS['status_key'] in first_order, f"Отсутствует ключ {KEYS['status_key']} в заказе"

    @allure.title("Получение ошибки при попытке получения заказа неавторизованным пользователем.")
    @allure.description("Тест для проверки получения ошибки при попытке получения заказа неавторизованным пользователем.")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    def test_get_user_orders_unauthorized_error_received(self):
        with allure.step("Отправить запрос на получение заказа не авторизованным пользователем."):
            response = requests.get(urls.ENDPOINTS['get_user_orders'])
            response_json = response.json()

        with allure.step("Проверить статус ответа."):
            assert response.status_code == 401, (
                f"Ожидался статус 401, получен {response.status_code}. Тело: {response.text}"
            )

        with allure.step("Проверить неуспешность запроса."):
            assert response_json[KEYS['success_key']] is False, (
                f"Ожидалось success=False, получено {response_json[KEYS['success_key']]}. "
                f"Тело: {response_json}"
            )

        with allure.step("Проверить сообщение об ошибке"):
            assert response_json[KEYS['message_key']] == ERROR_MESSAGES['unauthorized_get_update'], (
                f"Ожидалось сообщение '{ERROR_MESSAGES['unauthorized_get_update']}', "
                f"получено '{response_json[KEYS['message_key']]}'"
            )