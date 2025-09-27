import pytest
import socketio
import time
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