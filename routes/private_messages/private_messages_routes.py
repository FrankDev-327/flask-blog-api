from flask_restful import Api
from controllers.private_messages.private_messages_list_controller import (
    PrivateMessagesListController,
)


def register_private_messages_routes(api: Api):
    api.add_resource(
        PrivateMessagesListController,
        "/private-messages",
        endpoint="private_messages_all",
    )
