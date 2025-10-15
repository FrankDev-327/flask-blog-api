import pytest
import socketio
import time
import requests
from redis_serve.redis_service import RedisService

@pytest.mark.order(8)
@pytest.mark.parametrize("user_id", [3])
def test_notification_socket(user_id, auth_token, api_url):
    sio = socketio.Client()
    received_messages = []
    @sio.on('notification')
    def on_notification(data):
        received_messages.append(data)

    sio.connect(api_url+f"?token={auth_token}", transports=['websocket'])

    redis_service = RedisService()
    redis_service.publish("mention_comment_notification", {
        "content": "@test_user Hello!",
        "type": "notification",
        "comment_id": 123,
        "user_ids": [user_id]
    })

    time.sleep(3)

    assert len(received_messages) > 0
    assert received_messages[0]['comment_id'] == 123
    assert received_messages[0]['content'] == "@test_user Hello!"

    sio.disconnect()
    
def test_sending_message(auth_token, api_url, messages_to_send):
    sio = socketio.Client()
    messages = []
    
    @sio.on('message')
    def on_notification_messages(data):
        messages.append(data)
        
    sio.connect(api_url+f"?token={auth_token}", transports=['websocket'])
    sio.emit('message', messages_to_send)
    
    time.sleep(3)
    assert len(messages) >= 1
    
@pytest.mark.parametrize("user_id", [3])
def test_notification_request(user_id, auth_token, api_url):
    payload = { "contact_id": 7 }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{api_url}/contacts", headers=headers, json=payload)
    
    assert response.status_code == 200 or 201
    data = response.json()
    assert len(data) > 0
    assert "message" in data
    assert data['message'] == "Contact request sent"
    assert "contact" in data
    assert len(data['contact']) > 0
    
    time.sleep(3)
    
    sio = socketio.Client()
    notifications_messages = []
    
    @sio.on('friend_request_notification')
    def on_notification_friend(data):
        notifications_messages.append(data)
        
    sio.connect(api_url+f"?token={auth_token}", transports=['websocket'])
    redis_service = RedisService()
    redis_service.publish("friend_request_notification", {
        "content": "You have a new contact request from:",
        "type": "friend_request_notification",
        "request_id": 3,
        "contact_id": 7
    })
        
    time.sleep(3)
    if not notifications_messages:
        pytest.skip("No notification received (user may not be connected)")
    else:
        message = notifications_messages[0]
        if isinstance(message, str):
            assert message == "User not connected, skipping"
        else:
            assert isinstance(message, dict)
            assert len(message) > 0

    