from services.user_service import UserService
from base_resource import BaseResource 

class AuthUserController(BaseResource):
    method_map = { 
        'POST': 'checkExistinUser'
    }
    
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
    
    def checkExistinUser(self, user_body):
        return self.user_service.checkExistinUser(user_body)