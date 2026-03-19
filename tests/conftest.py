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


def test_create_new_user(user_data, auth_token, api_url):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{api_url}/user", headers=headers, json=user_data)
    assert response.status_code in (200, 201)
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "User created"


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
        "name": "test_user_20",
        "password": "123456789",
        "nick_name": "test_user_20",
        "email": "test_user_20@test.com",
    }


@pytest.fixture(scope="session")
def socket_client(auth_token):
    client = socketio.test_client(app, query_string=f"token={auth_token}")
    yield client
    client.disconnect()
