from base_resource import BaseResource
from services.comment_service import CommentService

class CommentUpdateController(BaseResource):
    method_map = { 'PUT': 'updateComment' }
    
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()
    
    def updateComment(self, comment_id, comment_body):
        return self.comment_service.updateComment(comment_id, comment_body)