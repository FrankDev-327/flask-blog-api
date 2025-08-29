from flask import jsonify
from connection import db
from logger.logging import LoggerApp
from services.user_service import UserService
from services.post_service import PostService
from models.comment_model import CommentModel  # Importing the db instance from connection.py

class CommentService:
    def __init__(self):
        self.comment_model = CommentModel
        self.logger = LoggerApp
        self.user_service = UserService()
        self.post_service = PostService()

    def getAllComments(self, post_id):
        comments = self.comment_model.query.filer(post_id = post_id).all()
        return [{'id': comment.id, 'content': comment.content, 'user_id': comment.user_id} for comment in comments], 200

    def createComment(self, commentBody):
        # Logic to create a new comment
        print(commentBody)
        if not commentBody or 'content' not in commentBody or 'user_id' not in commentBody or not 'post_id' in commentBody:
            return {'message': 'Content and user_id and post_id required'}, 400  
                
        new_comment = self.comment_model(content=commentBody['content'], user_id=commentBody['user_id'], post_id=commentBody['post_id'])
        try:
            db.session.add(new_comment)  # Add to DB session
            db.session.commit()           # Commit changes
            return {'message': 'Comment created', 'comment': new_comment.to_dict()}, 201
        except Exception as e:
            db.session.rollback()         # Rollback on error
            #self.logger.logInfo(e)
            return {'message': f'Error creating comment: {str(e)}'}, 500

    def put(self, comment_id):
        # Logic to update an existing comment
        return {'message': 'Comment updated', 'comment_id': comment_id}, 200

    def delete(self, comment_id):
        # Logic to delete a comment
        return {'message': 'Comment deleted', 'comment_id': comment_id}, 204