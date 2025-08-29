from services.user_service import UserService
from base_resource import BaseResource 

class UserController(BaseResource):
    method_map = {
        'GET': 'getUserByIdorAll',  
        'POST': 'createUser',
    }
    
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        
    def getUserByIdorAll(self, user_id):
        return self.user_service.getUserByIdorAll(user_id)
    
    def createUser(self, user_body):
        user = self.user_service.existUser(user_body.get('name'))
        if user:
            return {'message': 'User exists'}, 404
        return self.user_service.createUser(user_body)