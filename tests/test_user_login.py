import pytest
import requests
import allure
from helpers import LOGIN_USER_ENDPOINT


@allure.epic("Тесты API авторизации пользователя")
class TestUserLogin:

    @allure.feature("Авторизация")
    @allure.story("Успешный логин под существующим пользователем")
    def test_login_valid_user(self, base_url, registered_user):
        with allure.step("Формируем данные для входа"):
            email = registered_user["email"]
            password = registered_user["password"]
            data = {"email": email, "password": password}

        with allure.step("Отправляем POST-запрос на авторизацию"):
            response = requests.post(f"{base_url}{LOGIN_USER_ENDPOINT}", json=data)
            json_resp = response.json()

        with allure.step("Проверяем, что ответ имеет код 200"):
            assert response.status_code == 200

        with allure.step("Проверяем, что авторизация прошла успешно"):
            assert json_resp["success"] is True
            assert "accessToken" in json_resp
            assert "refreshToken" in json_resp
            assert json_resp["user"]["email"] == email

    @allure.feature("Авторизация")
    @allure.story("Логин с неверным логином или паролем")
    @pytest.mark.parametrize("email, password", [
        ("wrong_email@example.com", "password123"),
        ("sukhanova1234@gmail.com", "wrongpassword"),
        ("", "password123"),
        ("sukhanova1234@gmail.com", ""),
        ("", "")
    ])
    def test_login_invalid_credentials(self, base_url, email, password):
        data = {"email": email, "password": password}
        response = requests.post(f"{base_url}{LOGIN_USER_ENDPOINT}", json=data)
        json_resp = response.json()

        with allure.step("Проверяем, что получен код 401"):
            assert response.status_code == 401

        with allure.step("Проверяем сообщение об ошибке"):
            assert json_resp["success"] is False
            assert json_resp["message"] == "email or password are incorrect"