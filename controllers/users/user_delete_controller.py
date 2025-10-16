from flask_restful import Resource, request
from services.user_service import UserService
from middleware.check_token import require_token, check_user_role


class UserDeleteController(Resource):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @require_token
    @check_user_role
    def delete(self):
        """
        Delete a user
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
                  example: test_user_4444
                nick_name:
                  type: string
                  example: test_nich_name_user_4444
        responses:
          200:
            description: User successfully deleted
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User was deleted
          401:
            description: Unauthorized - invalid or missing token
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Unauthorized
          403:
            description: Forbidden - insufficient role
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Forbidden
          404:
            description: User not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: User not found
        """
        user_body = request.get_json(force=True)
        return self.user_service.delete_user(user_body)
