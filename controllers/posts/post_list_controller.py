from base_resource import BaseResource
from flask_restful import request
from middleware.check_token import require_token
from services.post_service import PostService

class PostListController(BaseResource):
    method_map = { 'GET': 'getAllPosts' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
    
    @require_token
    def getAllPosts(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return self.post_service.getAllPosts(page, per_page)
