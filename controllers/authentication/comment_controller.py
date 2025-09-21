from base_resource import BaseResource
from services.comment_service import CommentService

class CommentController(BaseResource):
    method_map = { 'POST': 'createComment'}
    
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()
        
    def createComment(self, comment_body):
        return self.comment_service.createComment(comment_body)