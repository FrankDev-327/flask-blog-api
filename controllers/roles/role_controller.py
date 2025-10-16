from flask_restful import Resource, request
from services.role_service import RoleService
from middleware.check_token import require_token, check_user_role


class RoleController(Resource):
    def __init__(self):
        super().__init__()
        self.role_service = RoleService()

    @require_token
    @check_user_role
    def post(self):
        """
        Assign a role to a user
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
            description: Role successfully created and assigned to user
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Role created
                role:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 11
                    role_name:
                      type: string
                      example: normal_user_2
                    user_id:
                      type: integer
                      example: 1
          400:
            description: Bad request due to missing data or duplicate assignment
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User was already assigned to this role
        """
        roleBody = request.get_json(force=True)
        return self.role_service.assignRoToUser(roleBody)
