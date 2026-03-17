import pytest
import requests
from app import app, socketio


@pytest.fixture(scope="session")
def api_url():
    return "http://127.0.0.1:5000/api"


@pytest.fixture(scope="session")
def create_new_interest():
    return {
        "interest_name": "test text",
        "description": "test_description",
    }


@pytest.fixture(scope="session")
def messages_to_send():
    return {
        "content": "test text",
        "sender_id": 3,
        "receiver_id": 13,
    }


@pytest.fixture(scope="session")
def auth_token(api_url):
    user_login = {"password": "123456789", "nick_name": "test_user_20"}
    response = requests.post(f"{api_url}/auth", json=user_login)
    assert response.status_code == 200
    assert len(response.json()["token"]) > 0
    parts = response.json()["token"].split(".")
    assert len(parts) == 3
    return response.json()["token"]


@pytest.fixture(scope="session")
def user_data():
    return {
        "name": "test_user_4444",
        "password": "123456789",
        "nick_name": "test_nich_name_user_4444",
        "email": "test_user_4444@test.com",
    }


@pytest.fixture(scope="session")
def socket_client(auth_token):
    client = socketio.test_client(app, query_string=f"token={auth_token}")
    yield client
    client.disconnect()
