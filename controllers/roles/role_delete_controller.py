from flask_restful import Resource, request
from services.role_service import RoleService
from middleware.check_token import require_token, check_user_role

class RoleDeleteController(Resource):    
    def __init__(self):
        super().__init__()
        self.role_service = RoleService()
        
    @require_token
    @check_user_role
    def delete(self):
        """
        Remove a role from a user
        ---
        tags:
          - Role
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - role_name
                - user_id
              properties:
                role_name:
                  type: string
                  example: "normal_user_2"
                user_id:
                  type: integer
                  example: 1
        responses:
          200:
            description: Role successfully removed from user
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Role removed successfully
          400:
            description: Bad request, missing fields or user has no role assigned
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Ths user does not have any role assigned
        """
        roleBody = request.get_json(force=True)
        return self.role_service.removeRoleFromUser(roleBody)
