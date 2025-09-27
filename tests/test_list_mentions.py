import pytest
import requests

@pytest.mark.order(9)
def test_list_mentions(auth_token, api_url):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{api_url}/mentions", headers=headers)
    assert response.status_code == 200 or 201
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert "mentioned_comment" in data
    assert data["message"] == "List of comments of a post"
    assert isinstance(data["mentioned_comment"], list)
    assert len(data["mentioned_comment"]) > 0