import os
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.mark.order(1)
def test_health_check_endpoint():
    response = requests.get(f"{BASE_URL}/health-check")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "OK"
    
@pytest.mark.order(2)
def test_auth_endpoint():
    response = requests.post(f"{BASE_URL}/auth", json={
        "password": "123456789",
        "nick_name": "test_user_20"
    })
  
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    assert len(data["token"]) > 0
    parts = data["token"].split(".")
    assert len(parts) == 3
    token_info_file = open("./token_test.txt", "w")
    assert token_info_file.write(data["token"]) > 0