from base_resource import BaseResource
from middleware.check_token import require_token
from services.post_service import PostService

class PostListController(BaseResource):
    method_map = { 'GET': 'getAllPosts' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
    
    @require_token
    def getAllPosts(self):
        return self.post_service.getAllPosts()
