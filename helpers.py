import requests
import time
from typing import Dict, List, Optional

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

ENDPOINTS = {
    "register": "/auth/register",
    "login": "/auth/login",
    "user": "/auth/user",
    "delete": "/auth/user",
    "orders": "/orders",
    "ingredients": "/ingredients"
}

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

def delete_user(access_token: str) -> requests.Response:

    headers = {"Authorization": access_token}
    return requests.delete(f"{BASE_URL}{ENDPOINTS['delete']}", headers=headers)

def get_user(access_token: str) -> requests.Response:

    headers = {"Authorization": access_token}
    return requests.get(f"{BASE_URL}{ENDPOINTS['user']}", headers=headers)

def update_user(access_token: str, data: Dict) -> requests.Response:

    headers = {"Authorization": access_token}
    return requests.patch(f"{BASE_URL}{ENDPOINTS['user']}", json=data, headers=headers)

def get_ingredients() -> List[str]:

    response = requests.get(f"{BASE_URL}{ENDPOINTS['ingredients']}")
    response.raise_for_status()
    data = response.json()
    return [item["_id"] for item in data.get("data", [])]

def create_order(ingredients: List[str], access_token: Optional[str] = None) -> requests.Response:

    headers = {}
    if access_token:
        headers["Authorization"] = access_token
    data = {"ingredients": ingredients}
    return requests.post(f"{BASE_URL}{ENDPOINTS['orders']}", json=data, headers=headers)

def get_orders(access_token: Optional[str] = None) -> requests.Response:

    headers = {}
    if access_token:
        headers["Authorization"] = access_token
    return requests.get(f"{BASE_URL}{ENDPOINTS['orders']}", headers=headers)