from flask_restful import Resource, request
from services.user_service import UserService
from middleware.check_token import require_token, check_user_role


class UserController(Resource):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @require_token
    @check_user_role
    def post(self):
        """
        Create a new user
        ---
        tags:
          - Users
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: test_user_30
                password:
                  type: string
                  example: 123456789
                nick_name:
                  type: string
                  example: test_nich_name_user_30
                email:
                  type: string
                  example: test_user_30@test.com
        responses:
          200:
            description: User successfully created
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User created
          400:
            description: Missing required fields
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Name and email required
          409:
            description: Conflict - user already exists
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User already exists
        """
        user_body = request.get_json(force=True)
        return self.user_service.createUser(user_body)
