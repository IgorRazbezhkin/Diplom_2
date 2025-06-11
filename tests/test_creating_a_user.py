import pytest
import allure
import urls
from helpers import register_user, get_json_response
from data import ERROR_MESSAGES, KEYS


@allure.suite("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя.")
    @allure.description("Тест для проверки успешного создание нового уникального пользователя.")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    def test_create_unique_user_success(self, unique_user):
        with allure.step("Отправить запрос на регистрацию пользователя"):
            response = register_user(unique_user)
            response_json = get_json_response(response)

        with allure.step("Проверить статус ответа"):
            assert response.status_code == 200, (
                f"Ошибка при создании пользователя: статус {response.status_code}, тело: {response.text}"
            )

        with allure.step("Проверить успешность запроса."):
            assert response_json.get(KEYS['success_key']) is True, (
                f"Создание пользователя не удалось: {response_json}"
            )

        with allure.step("Проверить наличие ключа 'user' в ответе"):
            user_info = response_json.get(KEYS['user_key'])
            assert user_info is not None, "В ответе отсутствует ключ 'user'"

        with allure.step("Проверить структуру данных внутри 'user'"):
            for key in ["email", "name"]:
                assert key in user_info, f"В ответе отсутствует ключ '{key}' внутри 'user'"

        with allure.step("Проверить совпадение email и имени пользователя"):
            email_response = user_info["email"]
            name_response = user_info["name"]
            expected_email = unique_user["email"]
            expected_name = unique_user["name"]

            assert email_response.lower() == expected_email.lower(), (
                f"Email не совпадает: ожидаемый '{expected_email}', полученный '{email_response}'"
            )
            assert name_response == expected_name, (
                f"Имя не совпадает: ожидаемое '{expected_name}', полученное '{name_response}'"
            )

    @allure.title("Получение ошибки при создании пользователя с существующим email.")
    @allure.description("Тест для проверки получения ошибки при создании пользователя с существующим email.")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    def test_create_user_with_existing_email_error_received(self, registered_user):
        with allure.step("Зарегистрировать пользователя с уже существующим email"):
            response = register_user(registered_user)
            response_json = get_json_response(response)

        with allure.step("Проверить код и сообщение об ошибке"):
            message = response_json.get(KEYS['message_key'])
            assert (response.status_code, message) == (403, ERROR_MESSAGES['user_exists']), (
                f"Ожидался статус 403 и сообщение '{ERROR_MESSAGES['user_exists']}', "
                f"Получен статус {response.status_code} и сообщение '{message}'. Тело: {response.text}"
            )

    @allure.title("Получение ошибки при создании пользователя с отсутствующими обязательными данными.")
    @allure.description("Тест для проверки получения ошибки при создании пользователя с отсутствующими обязательными данными.")
    @allure.link(urls.API_DOCUMENTATION, name="API документация")

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])

    def test_registration_missing_fields_error_received(self, missing_field, unique_user):
        with allure.step("Создать копию данных пользователя и удалить одно из обязательных полей."):
            user_data = unique_user.copy()
            user_data.pop(missing_field)

        with allure.step("Отправить запрос на регистрацию без одного из обязательных полей."):
            response = register_user(user_data)
            response_json = get_json_response(response)

        with allure.step("Проверить код и сообщение об ошибке"):
            message = response_json.get(KEYS['message_key'])
            assert (response.status_code, message) == (403, ERROR_MESSAGES['missing_fields']), (
                f"Ожидался статус 403 и сообщение '{ERROR_MESSAGES['missing_fields']}', "
                f"Получен статус {response.status_code} и сообщение '{message}'. Тело: {response.text}"
            )