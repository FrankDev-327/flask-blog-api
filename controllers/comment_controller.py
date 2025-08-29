from base_resource import BaseResource
from services.comment_service import CommentService

class CommentController(BaseResource):
    method_map = {
        'GET': 'getAllCommentsByPostId',
        'POST': 'createComment',
        'PUT': 'updateComment',
    }
    
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()
        
    def getAllCommentsByPostId(self):
        return self.comment_service.getAllCommentsByPostId()
    
    def createComment(self, comment_body):
        return self.comment_service.createComment(comment_body)
    
    def updateComment(self, comment_id, comment_body):
        return self.comment_service.updateComment(comment_id, comment_body)