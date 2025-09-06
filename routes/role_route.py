from flask_restful import Api
from controllers.role_controller import RoleController

def register_role_route(api: Api):
    api.add_resource(RoleController, '/roles', methods=['POST'], endpoint='roles')