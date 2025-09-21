from connection import db
from utils.helpers import Helper
from logger.logging import LoggerApp
from services.user_service import UserService
from services.post_service import PostService
from models.comment_model import CommentModel 
from middleware.check_token import require_token
from sqlalchemy import select, insert, delete, update

helper = Helper()

class CommentService:
    def __init__(self):
        self.logger = LoggerApp()
        self.comment_model = CommentModel

    @require_token
    def createComment(self, commentBody):
        if not commentBody or 'content' not in commentBody or 'user_id' not in commentBody or not 'post_id' in commentBody:
            return {'message': 'Content and user_id and post_id required'}, 400 
         
        try:    
            stmt = (
                insert(CommentModel).values(
                    content=commentBody['content'], 
                    user_id=commentBody['user_id'], 
                    post_id=commentBody['post_id']
                )
                .returning(CommentModel)
            )
        
            result = db.session.execute(stmt)
            row = result.fetchone()
            db.session.commit()       
            new_comment = row[0]
            
            return {
                'message': 'Comment created', 
                'comment': {
                    "id": new_comment.id,
                    "content": new_comment.content,
                    "post_id": new_comment.post_id,
                    "user_id": new_comment.user_id,
                    "created_at": helper.formatting_time(new_comment.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": helper.formatting_time(new_comment.updated_at, "%Y-%m-%d %H:%M:%S")
                }
            }, 201
        except Exception as e:
            db.session.rollback() 
            return {'message': f'Error creating comment: {str(e)}'}, 500

    @require_token
    def getCommentById(self, comment_id):
        try:
            stmt = (select(CommentModel).where(CommentModel.id == comment_id))
            comment = db.session.execute(stmt).scalar_one_or_none()
            if comment:
                return {
                    "id": comment.id,
                    "content": comment.content,
                    "post_id": comment.post_id,
                    "user_id": comment.user_id,
                    "created_at": helper.formatting_time(comment.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": helper.formatting_time(comment.updated_at, "%Y-%m-%d %H:%M:%S")
                }, 200
            return {'message': 'Comment not found'}, 404
        except Exception as e:
            db.session.rollback() 
            return {'message': f'Error getting details comment: {str(e)}'}, 500

    @require_token
    def updateComment(self, comment_id, commentBody):
        if not isinstance(commentBody, dict):
            return {'message': 'Invalid request body format'}, 400
        
        try:
            update_stmt = (
                update(CommentModel)
                .where(CommentModel.id == comment_id)
                .values(
                    content=commentBody['content']
                ).returning(CommentModel)
            )
            
            result = db.session.execute(update_stmt)
            row = result.fetchone()
            db.session.commit()       
            updated_comment = row[0]
            
            return {
                'message': 'Comment updated', 
                'comment': {
                    "id": updated_comment.id,
                    "content": updated_comment.content,
                    "post_id": updated_comment.post_id,
                    "user_id": updated_comment.user_id,
                    "created_at": helper.formatting_time(updated_comment.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": helper.formatting_time(updated_comment.updated_at, "%Y-%m-%d %H:%M:%S")
                }
            }, 200
        except Exception as e:
            db.session.rollback() 
            return {'message': f'Error updating comment: {str(e)}'}, 500

    @require_token
    def delete(self, comment_id):
        return {'message': 'Comment deleted', 'comment_id': comment_id}, 204