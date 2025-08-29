from base_resource import BaseResource
from services.comment_service import CommentService

class CommentController(BaseResource):
    method_map = {
        'GET': 'getAllComments',
        'POST': 'createComment'
    }
    
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()
        
    def getAllComments(self):
        return self.comment_service.getAllComments()
    
    def createComment(self, comment_body):
        return self.comment_service.createComment(comment_body)