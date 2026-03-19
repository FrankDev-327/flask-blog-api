from flask_restful import Api
from controllers.notifications.notifications_list_user import NotificationController


def register_notifications_route(api: Api):
    api.add_resource(
        NotificationController, "/notifications", endpoint="notifications_list"
    )
