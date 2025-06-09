import pytest
import allure
from helpers import register_user


@allure.epic("Тесты API регистрации пользователя")
class TestUserRegistration:

    @allure.feature("Создание пользователя")
    @allure.story("Успешное создание уникального пользователя")
    def test_create_unique_user(self, unique_email):
        password = "password12345"
        name = "sukhanova"

        response = register_user(unique_email, password, name)

        with allure.step("Проверяем, что код ответа 200 или 201"):
            assert response.status_code in (200, 201)

        with allure.step("Проверяем, что в ответе success=True"):
            json_resp = response.json()
            assert json_resp.get("success") is True

    @allure.feature("Создание пользователя")
    @allure.story("Создание пользователя, который уже существует")
    def test_create_existing_user(self, registered_user):

        response = register_user(
            registered_user["email"],
            registered_user["password"],
            registered_user["name"]
        )

        with allure.step("Проверяем, что код ответа 403"):
            assert response.status_code == 403

        with allure.step("Проверяем, что сообщение 'User already exists'"):
            json_resp = response.json()
            assert json_resp.get("success") is False
            assert json_resp.get("message") == "User already exists"

    @allure.feature("Создание пользователя")
    @allure.story("Создание пользователя с отсутствующим обязательным полем")
    @pytest.mark.parametrize("missing_field, payload", [
        ("email", {"password": "password12345", "name": "sukhanova"}),
        ("password", {"email": "sukhanova1234@gmail.com", "name": "sukhanova"}),
        ("name", {"email": "sukhanova1234@gmail.com", "password": "password12345"}),
    ])
    def test_create_user_missing_fields(self, missing_field, payload):
        response = register_user(
            payload.get("email", ""),
            payload.get("password", ""),
            payload.get("name", "")
        )

        with allure.step("Проверяем, что код ответа 403"):
            assert response.status_code == 403

        with allure.step("Проверяем, что сообщение об обязательных полях"):
            json_resp = response.json()
            assert json_resp.get("success") is False
            assert json_resp.get("message") == "Email, password and name are required fields"