from middleware.check_token import generateToken
from flask_restful import Resource, request
from services.user_service import UserService

class AuthUserController(Resource):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
    
    def post(self):
        """
        Authenticate user and return JWT token
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - nick_name
                - password
              properties:
                nick_name:
                  type: string
                  example: test_user_20
                password:
                  type: string
                  example: 123456789
        responses:
          200:
            description: User successfully authenticated
            schema:
              type: object
              properties:
                token:
                  type: string
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywibmFtZS..."
          404:
            description: User not found or wrong password
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "user not found or wrong password"
        """
        user_body = request.get_json(force=True)
        user = self.user_service.checkExistinUser(user_body)
        token = generateToken(user)
        return {'token': token}
