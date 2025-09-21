from services.post_service import PostService
from base_resource import BaseResource

class PostCreateController(BaseResource):
    method_map = { 'POST': 'createPost'}
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
    
    def createPost(self, post_body):
        return self.post_service.createPost(post_body)