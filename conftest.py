import pytest
from helpers import (
    generate_unique_email,
    register_user,
    login_user,
    get_ingredients,
    delete_user
)


@pytest.fixture(scope="session")
def base_url():
    yield "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture
def unique_email():
    yield generate_unique_email()


@pytest.fixture
def registered_user():
    email = generate_unique_email()
    password = "password12345"
    name = "Test User"

    response = register_user(email, password, name)
    assert response.status_code in (200, 201), "Не удалось создать пользователя"

    user_data = {
        "email": email,
        "password": password,
        "name": name,
        "access_token": None
    }

    login_resp = login_user(email, password)
    if login_resp.status_code == 200:
        user_data["access_token"] = login_resp.json().get("accessToken")

    yield user_data

    if user_data["access_token"]:
        delete_response = delete_user(user_data["access_token"])
        assert delete_response.status_code == 202, "Не удалось удалить пользователя"


@pytest.fixture
def access_token(registered_user):
    response = login_user(registered_user["email"], registered_user["password"])
    assert response.status_code == 200, "Не удалось залогиниться"
    json_resp = response.json()
    token = json_resp.get("accessToken")
    assert token is not None, "Токен доступа не получен"
    yield token


@pytest.fixture
def auth_token():
    email = generate_unique_email()
    password = "password123"
    name = "Fixture User"

    response = register_user(email, password, name)
    assert response.status_code in (200, 201), "Не удалось создать пользователя для auth_token"

    login_resp = login_user(email, password)
    assert login_resp.status_code == 200, "Не удалось залогиниться для auth_token"
    token = login_resp.json().get("accessToken")
    assert token is not None, "Токен доступа не получен для auth_token"

    yield token

    delete_response = delete_user(token)
    assert delete_response.status_code == 202, "Не удалось удалить тестового пользователя"


@pytest.fixture(scope="session")
def ingredients_ids():
    yield get_ingredients()