from flask_restful import Api
from controllers.roles.role_controller import RoleController
from controllers.roles.role_delete_controller import RoleDeleteController

def register_role_route(api: Api):
    api.add_resource(RoleController, '/roles', methods=['POST'], endpoint='roles')
    api.add_resource(RoleDeleteController, '/roles', methods=['DELETE'], endpoint='roles_update')