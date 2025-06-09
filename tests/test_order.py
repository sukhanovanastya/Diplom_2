import pytest
import allure
from helpers import create_order

@allure.epic("Тесты API заказов")
class TestCreateOrderParam:

    @pytest.mark.parametrize(
        "ingredients, token, expected_status, expected_success, expected_message",
        [
            (["valid_ingredient_id_1", "valid_ingredient_id_2"], "valid_token_placeholder", 200, True, None),
            (["valid_ingredient_id_1"], None, 200, True, None),
            (["invalid_ingredient_id"], "valid_token_placeholder", 400, False, "Ingredient ids must be provided"),
            (["valid_ingredient_id_1"], "invalid_token_placeholder", 500, None, None),
        ]
    )
    @allure.story("Параметризованный тест создания заказа")
    def test_create_order_parametrized(self, auth_token, ingredients, token, expected_status, expected_success, expected_message):
        actual_token = auth_token if token == "valid_token_placeholder" else token

        response = create_order(ingredients=ingredients, token=actual_token)

        assert response.status_code == expected_status

        json_resp = response.json()

        if expected_success is not None:
            assert json_resp.get("success") == expected_success

        if expected_message is not None:
            assert json_resp.get("message") == expected_message