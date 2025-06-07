import pytest
import allure
from helpers import update_user, login_user, register_user, generate_unique_email

@allure.epic("Тесты API изменения данных пользователя")
class TestUserUpdate:

    @allure.feature("Изменение данных пользователя")
    @allure.story("Успешное изменение email и имени с авторизацией")
    def test_update_user_authorized(self, auth_token):
        new_email = generate_unique_email()
        new_name = "Updated Name"

        update_resp = update_user(auth_token, {"email": new_email, "name": new_name})
        assert update_resp.status_code == 200

        json_resp = update_resp.json()
        with allure.step("Проверяем success=True и обновлённые поля"):
            assert json_resp.get("success") is True
            user = json_resp.get("user")
            assert user is not None
            assert user.get("email") == new_email
            assert user.get("name") == new_name

    @allure.feature("Изменение данных пользователя")
    @allure.story("Попытка изменения данных без авторизации")
    def test_update_user_unauthorized(self):
        new_email = generate_unique_email()
        new_name = "Updated Name"

        update_resp = update_user(token="", data={"email": new_email, "name": new_name})
        assert update_resp.status_code == 401

        json_resp = update_resp.json()
        with allure.step("Проверяем сообщение об ошибке авторизации"):
            assert json_resp.get("success") is False
            assert json_resp.get("message") == "You should be authorised"

    @allure.feature("Изменение данных пользователя")
    @allure.story("Попытка изменить email на существующий")
    def test_update_user_existing_email(self, auth_token):
        existing_email = generate_unique_email()
        password = "password12345"
        name = "Existing User"
        register_resp = register_user(existing_email, password, name)
        assert register_resp.status_code in (200, 201)

        update_resp = update_user(auth_token, {"email": existing_email, "name": "New Name"})

        assert update_resp.status_code == 403

        json_resp = update_resp.json()
        with allure.step("Проверяем сообщение о существующем email"):
            assert json_resp.get("success") is False
            assert json_resp.get("message") == "User with such email already exists"