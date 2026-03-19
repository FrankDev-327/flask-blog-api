import pytest
import requests


@pytest.mark.order(3)
def test_user_exists(user_data, auth_token, api_url):
    assert len(auth_token) > 0
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{api_url}/user", headers=headers, json=user_data)
    assert response.status_code == 409
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "User already exists"
