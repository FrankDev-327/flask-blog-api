from middleware.check_token import generateToken
from base_resource import BaseResource 
from services.user_service import UserService


class AuthUserController(BaseResource):
    method_map = { 
        'POST': 'checkExistinUser'
    }
    
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
    
    def checkExistinUser(self, user_body):
        user = self.user_service.checkExistinUser(user_body)
        token = generateToken(user[0]['user'])
        return {'token': token}