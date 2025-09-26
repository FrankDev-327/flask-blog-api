import os
import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:5000/api"

@pytest.mark.order(5)
def test_delete_user():
   
    with open("./token_test.txt", "r") as f:
        token_info_file = f.read().strip()
        
    with open("./user_to_test.json", "r") as f:
        user_info = json.load(f)  
        
    user_to_be_deleted = {
        "name": user_info['name'],
        "nick_name":user_info['nick_name']
    }
    
    headers = {"Authorization": f"Bearer {token_info_file}"}
    response = requests.delete(f"{BASE_URL}/user", headers=headers, json=user_to_be_deleted)
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data["message"], str)
    assert data["message"] == "User was deleted"
    os.remove("./token_test.txt")
    os.remove("./user_to_test.json")