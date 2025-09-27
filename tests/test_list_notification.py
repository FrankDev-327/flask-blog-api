import pytest
import requests

@pytest.mark.order(8)
def test_list_notification(auth_token, api_url):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{api_url}/notifications", headers=headers)
    assert response.status_code == 200 or 201
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "notifications" in data
    assert data["message"] == "List of notifications"
    assert isinstance(data["notifications"], list)
    assert len(data["notifications"]) > 0
    