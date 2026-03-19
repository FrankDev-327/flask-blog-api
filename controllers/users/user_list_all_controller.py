from flask_restful import Resource
from services.user_service import UserService
from middleware.check_token import require_token, check_user_role


class UserListController(Resource):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()

    @require_token
    @check_user_role
    def get(self):
        """
        Get all users
        ---
        tags:
          - Users
        responses:
          200:
            description: List of all users
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: test_user_4
                  nick_name:
                    type: string
                    example: null
                  email:
                    type: string
                    example: test_user_4@test.com
            examples:
              application/json: [
                {
                  "id": 1,
                  "name": "test_user_4",
                  "nick_name": null,
                  "email": "test_user_4@test.com"
                },
                {
                  "id": 2,
                  "name": "test_user_5",
                  "nick_name": null,
                  "email": "test_user_5@test.com"
                }
              ]
        """
        return self.user_service.getAllUsers()
