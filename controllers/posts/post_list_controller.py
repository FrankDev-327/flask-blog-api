from base_resource import BaseResource
from services.post_service import PostService

class PostListController(BaseResource):
    method_map = { 'GET': 'getAllPosts' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    def getAllPosts(self):
        return self.post_service.getAllPosts()
