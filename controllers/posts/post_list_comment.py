from flask_restful import request
from base_resource import BaseResource
from middleware.check_token import require_token
from services.post_service import PostService

class PostListComments(BaseResource):
    method_map = { 'GET': 'listAllCommentByPostId' }
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    @require_token
    def listAllCommentByPostId(self, post_id):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return self.post_service.listAllCommentByPostId(post_id, page, per_page)