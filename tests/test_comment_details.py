import pytest
import requests


@pytest.mark.order(11)
@pytest.mark.parametrize("comment_id", [140, 20])
def test_comment_details(auth_token, api_url, comment_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"{api_url}/comments/{comment_id}", headers=headers)
    assert response.status_code == 200 or 201
    data = response.json()
    assert len(data) > 0
    assert "id" in data
    assert "content" in data
    assert "post_id" in data
    assert len(data["children"]) > 0
