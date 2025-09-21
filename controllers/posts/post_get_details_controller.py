from base_resource import BaseResource 
from services.post_service import PostService

class PostGetDetailsController(BaseResource):
    method_map = { 'GET': 'getPostById' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    def getPostById(self, post_id):
        return self.post_service.getPostById(post_id)