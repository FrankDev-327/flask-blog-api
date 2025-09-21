from base_resource import BaseResource
from middleware.check_token import require_token
from services.comment_service import CommentService

class CommentController(BaseResource):
    method_map = { 'POST': 'createComment'}
    
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()
    
    @require_token
    def createComment(self, comment_body):
        return self.comment_service.createComment(comment_body)