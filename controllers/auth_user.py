from middleware.check_token import generateToken
from base_resource import BaseResource 
from services.user_service import UserService
from run_server import prom_service

class AuthUserController(BaseResource):
    method_map = { 
        'POST': 'checkExistinUser'
    }
    
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
    
    def checkExistinUser(self, user_body):
        user = self.user_service.checkExistinUser(user_body)
        token = generateToken(user)
        prom_service.log_count_request('POST', '/api/auth/login', 200)
        return {'token': token}