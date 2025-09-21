from base_resource import BaseResource
from middleware.check_token import require_token
from services.post_service import PostService

class PostUpdateController(BaseResource):
    method_map = { 'PUT': 'updatePost' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    @require_token
    def updatePost(self, post_id, post_body):
        return self.post_service.updatePost(post_id, post_body)