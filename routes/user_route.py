from flask_restful import Api
from controllers.user_controller import UserController

def register_user_routes(api: Api):
    api.add_resource(UserController, '/user', methods=['POST'], endpoint='user_create')
    api.add_resource(UserController, '/user/<int:user_id>' , '/user', methods=['GET'], endpoint='user_get_or_all')
    #api.add_resource(UserController, '/user', methods=['GET'], endpoint='user_all')
    