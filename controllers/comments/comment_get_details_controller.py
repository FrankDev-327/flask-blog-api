from base_resource import BaseResource 
from services.comment_service import CommentService

class CommentGetDetailsController(BaseResource):
    method_map = { 'GET': 'getCommentById'}
    
    def __init__(self):
        super().__init__()
        self.comment_servie = CommentService()
        
    def getCommentById(self, comment_id):
        return self.comment_servie.getCommentById(comment_id)