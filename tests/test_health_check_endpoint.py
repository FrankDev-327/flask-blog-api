import pytest
import requests


@pytest.mark.order(1)
def test_health_check_endpoint(api_url):
    response = requests.get(f"{api_url}/health-check")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "OK"