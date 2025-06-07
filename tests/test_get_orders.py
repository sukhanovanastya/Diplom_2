import pytest
import allure
from helpers import get_orders

@allure.epic("Тесты API заказов")
@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.story("Получение заказов с авторизацией")
    def test_get_orders_authorized(self, auth_token):
        response = get_orders(token=auth_token)

        with allure.step("Проверяем, что код ответа 200"):
            assert response.status_code == 200

        json_resp = response.json()

        with allure.step("Проверяем, что success == True"):
            assert json_resp.get("success") is True

        with allure.step("Проверяем наличие списка orders и его тип"):
            orders = json_resp.get("orders")
            assert isinstance(orders, list)

        with allure.step("Проверяем, что каждый заказ содержит необходимые поля"):
            for order in orders:
                assert "ingredients" in order
                assert isinstance(order["ingredients"], list)
                assert "_id" in order
                assert "status" in order
                assert "number" in order
                assert "createdAt" in order
                assert "updatedAt" in order

    @allure.story("Получение заказов без авторизации")
    def test_get_orders_unauthorized(self):
        response = get_orders()

        with allure.step("Проверяем, что код ответа 401"):
            assert response.status_code == 401

        json_resp = response.json()

        with allure.step("Проверяем, что success == False и сообщение об ошибке"):
            assert json_resp.get("success") is False
            assert json_resp.get("message") == "You should be authorised"