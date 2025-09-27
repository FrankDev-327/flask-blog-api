import pytest
from dotenv import load_dotenv 

load_dotenv()

@pytest.mark.order(6)
def test_socket_connection(socket_client):
    assert socket_client.is_connected()

@pytest.mark.order(7)
def test_send_message(socket_client):
    socket_client.emit("message", {"message": "hello from pytest"})
    received = socket_client.get_received()
    assert any(event["name"] == "message" for event in received)
    