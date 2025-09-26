import os
import pytest
import json
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.mark.order(3)
def test_create_new_user():
    user_to_be_created = {
        "name": "test_user_4444",
        "password": "123456789",
        "nick_name":"test_nich_name_user_4444",
        "email": "test_user_4444@test.com"
    }
    
    with open("./token_test.txt", "r") as f:
        token_info_file = f.read().strip()
    assert len(token_info_file) > 0
    headers = {"Authorization": f"Bearer {token_info_file}"}
    
    response = requests.post(f"{BASE_URL}/user", headers=headers, json=user_to_be_created)
    assert response.status_code == 200 or 201
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "User created"
    with open('user_to_test.json', 'w') as f:
        json.dump(user_to_be_created, f)
    
