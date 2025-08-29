from base_resource import BaseResource 
from services.user_service import UserService

class UserListPostAndCommentController(BaseResource):
    method_map = {
        'GET': 'getUserByIdOrAll',  
    }
     
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        
    def getUserByIdOrAll(self, user_id):
        return self.user_service.getUserByIdOrAll(user_id)