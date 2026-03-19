# import pytest
# import requests


# @pytest.mark.order(2)
# def test_create_new_user(user_data, auth_token, api_url):
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     response = requests.post(f"{api_url}/user", headers=headers, json=user_data)
#     assert response.status_code in (200, 201)
#     data = response.json()
#     assert "message" in data
#     assert isinstance(data["message"], str)
#     assert data["message"] == "User created"
