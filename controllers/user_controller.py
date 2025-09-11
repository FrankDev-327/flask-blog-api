from services.user_service import UserService
from base_resource import BaseResource 
from middleware.check_token import require_token, check_user_role

class UserController(BaseResource):
    method_map = {
        'GET': 'getAllUsers',  
        'POST': 'createUser',
    }
    
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        
    
    @require_token
    @check_user_role
    def getAllUsers(self):
        return self.user_service.getAllUsers()
    
    @require_token
    @check_user_role
    def createUser(self, user_body):
        user = self.user_service.existUser(user_body.get('name'))
        if user:
            return {'message': 'User exists'}, 404
        return self.user_service.createUser(user_body)