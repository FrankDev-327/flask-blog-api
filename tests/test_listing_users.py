import pytest
import requests

@pytest.mark.order(10)
def test_listing_users(auth_token, api_url):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{api_url}/user", headers=headers)
        assert response.status_code in (200, 201)
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0