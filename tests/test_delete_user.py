import pytest
import requests


@pytest.fixture
def user_delete_data():
    return {
        "name": "test_user_4444",
        "nick_name": "test_nich_name_user_4444",
    }


@pytest.mark.order(5)
def test_delete_user(user_delete_data, auth_token, api_url):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.delete(
        f"{api_url}/user", headers=headers, json=user_delete_data
    )
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["message"], str)
    assert data["message"] == "User was deleted"
