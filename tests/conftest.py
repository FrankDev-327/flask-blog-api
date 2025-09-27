import pytest
import requests
from app import app, socketio

@pytest.fixture(scope="session")
def user_login():
    return {
        "password": "123456789",
        "nick_name": "test_user_20"
    }

@pytest.fixture(scope="session")
def api_url():
    return "http://127.0.0.1:5000/api"

@pytest.fixture(scope="session")
def auth_token(user_login, api_url):
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
        "nick_name":"test_nich_name_user_4444",
        "email": "test_user_4444@test.com"
    }
    
@pytest.fixture(scope="session")
def user_delete_data():
    return {
        "name": "test_user_4444",
        "nick_name":"test_nich_name_user_4444",
    }
    
@pytest.fixture(scope="session")
def comment_data():
    return {
        "content": "@test_user_20 test extract user from content chiild",
        "post_id": 1,
        "user_id": 2,
        "parent_id": 140,
        "user_mentioned_ids": [3, 13]
    }

@pytest.fixture(scope="session")
def socket_client(auth_token):
    client = socketio.test_client(app, query_string=f"token={auth_token}")
    yield client
    client.disconnect()