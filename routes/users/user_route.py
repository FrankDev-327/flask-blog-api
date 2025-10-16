from flask_restful import Api
from controllers.users.user_controller import UserController
from controllers.users.user_delete_controller import UserDeleteController
from controllers.users.user_list_all_controller import UserListController


def register_user_routes(api: Api):
    api.add_resource(UserController, "/user", endpoint="user_create")
    api.add_resource(UserListController, "/user", endpoint="user_all")
    api.add_resource(UserDeleteController, "/user", endpoint="user_delete")
