import os
import pytest
import json
import requests


@pytest.mark.order(4)
def test_create_comment(comment_data, auth_token, api_url):            
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{api_url}/comments", headers=headers, json=comment_data)
    assert response.status_code == 200 or 201
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert data["message"] == "Comment created"
    assert len(data["comment"]) > 0
    assert "id" in data["comment"]
    assert "content" in data["comment"]
    assert "post_id" in data["comment"]
    assert "user_id" in data["comment"]
    assert "parent_id" in data["comment"]
    assert "created_at" in data["comment"]
    assert "updated_at" in data["comment"]
    
    
    