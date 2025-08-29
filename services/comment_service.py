from connection import db
from logger.logging import LoggerApp
from services.user_service import UserService
from services.post_service import PostService
from models.comment_model import CommentModel 

class CommentService:
    def __init__(self):
        self.logger = LoggerApp
        self.comment_model = CommentModel
        self.user_service = UserService()
        self.post_service = PostService()

    def getAllCommentsByPostId(self, post_id):
        comments = self.comment_model.query.filer(post_id = post_id).all()
        return [{'id': comment.id, 'content': comment.content, 'user_id': comment.user_id} for comment in comments], 200

    def createComment(self, commentBody):
        if not commentBody or 'content' not in commentBody or 'user_id' not in commentBody or not 'post_id' in commentBody:
            return {'message': 'Content and user_id and post_id required'}, 400  
                
        new_comment = self.comment_model(content=commentBody['content'], user_id=commentBody['user_id'], post_id=commentBody['post_id'])
        try:
            db.session.add(new_comment) 
            db.session.commit()         
            return {'message': 'Comment created', 'comment': new_comment.to_dict()}, 201
        except Exception as e:
            db.session.rollback() 
            return {'message': f'Error creating comment: {str(e)}'}, 500

    def getCommentById(self, comment_id):
        comment = self.comment_model.query.get(comment_id)
        if comment:
            return comment.to_dict(), 200
        return {'message': 'Comment not found'}, 404

    def updateComment(self, comment_id, commentBody):
        comment = self.getCommentById(comment_id)
        if not comment:
            return {'message': 'Comment not found'}, 404
        
        commentUpdated = self.comment_model.update(comment_id, commentBody['content'])
        return {'message': 'Comment updated', 'comment': commentUpdated.to_dict()}, 200

    def delete(self, comment_id):
        return {'message': 'Comment deleted', 'comment_id': comment_id}, 204