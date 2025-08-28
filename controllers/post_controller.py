from services.post_service import PostService
from base_resource import BaseResource

class PostController(BaseResource):
    method_map = {
        'GET': 'getPostById',
        'POST': 'createPost',
        'GET': 'getAllPosts',
    }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    def getPostById(self, post_id):
        return self.post_service.getPostById(post_id)   
    
    def getAllPosts(self):
        return self.post_service.getAllPosts()
    
    def createPost(self, post_body):
        return self.post_service.createPost(post_body)