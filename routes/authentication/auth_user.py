from flask_restful import Api
from controllers.authentication.auth_user import AuthUserController

def register_auth_user(api: Api):
    api.add_resource(AuthUserController, '/auth', methods=['POST'], endpoint='auth_user')