import os
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.mark.order(4)
def test_user_exists():
    user_to_be_created = {
        "name": "test_user_32",
        "password": "123456789",
        "nick_name":"test_nich_name_user_32",
        "email": "test_user_32@test.com"
    }
    
    with open("./token_test.txt", "r") as f:
        token_info_file = f.read().strip()
    assert len(token_info_file) > 0 
    headers = {"Authorization": f"Bearer {token_info_file}"}
    response = requests.post(f"{BASE_URL}/user", headers=headers, json=user_to_be_created)
    assert response.status_code == 409
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "User already exists"
    
