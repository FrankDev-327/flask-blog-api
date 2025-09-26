import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

def test_health_check_endpoint():
    response = requests.get(f"{BASE_URL}/health-check")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "OK"
    
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