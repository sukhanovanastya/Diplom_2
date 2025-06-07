import requests
import time

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

ENDPOINTS = {
    "register": "/auth/register",
    "login": "/auth/login",
    "user": "/auth/user",
    "orders": "/orders",
    "ingredients": "/ingredients"
}

LOGIN_USER_ENDPOINT = ENDPOINTS["login"]

def generate_unique_email() -> str:
    return f"user_{int(time.time() * 1000)}@example.com"

def register_user(email: str, password: str, name: str) -> requests.Response:
    data = {
        "email": email,
        "password": password,
        "name": name
    }
    return requests.post(f"{BASE_URL}{ENDPOINTS['register']}", json=data)

def login_user(email: str, password: str) -> requests.Response:
    data = {
        "email": email,
        "password": password
    }
    return requests.post(f"{BASE_URL}{ENDPOINTS['login']}", json=data)

def get_user(token: str) -> requests.Response:
    headers = {"Authorization": token}
    return requests.get(f"{BASE_URL}{ENDPOINTS['user']}", headers=headers)

def update_user(token: str, data: dict) -> requests.Response:
    headers = {"Authorization": token}
    return requests.patch(f"{BASE_URL}{ENDPOINTS['user']}", json=data, headers=headers)

def get_ingredients() -> list:
    response = requests.get(f"{BASE_URL}{ENDPOINTS['ingredients']}")
    response.raise_for_status()
    data = response.json()
    return [item["_id"] for item in data.get("data", [])]

def create_order(ingredients: list, token: str = None) -> requests.Response:
    headers = {}
    if token:
        headers["Authorization"] = token
    data = {"ingredients": ingredients}
    return requests.post(f"{BASE_URL}{ENDPOINTS['orders']}", json=data, headers=headers)

def get_orders(token: str = None) -> requests.Response:
    headers = {}
    if token:
        headers["Authorization"] = token
    return requests.get(f"{BASE_URL}{ENDPOINTS['orders']}", headers=headers)