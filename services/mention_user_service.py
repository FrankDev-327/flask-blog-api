from connection import db
from flask import jsonify
from utils.helpers import Helper
from sqlalchemy.orm import aliased
from logger.logging import LoggerApp
from sqlalchemy import insert, select
from models.comment_model import CommentModel
from services.user_service import UserService
from models.mentions_model import MentionModel
#from services.rabbit_mq_service import RabbitMqService

helper = Helper()

class MentionService:
    def __init__(self):
        self.logger = LoggerApp()
        self.user_service = UserService()
        #self.rabbit_service = RabbitMqService()
        
    def create_mention(self, content, comment_id):
        try:
            users_mentioned = helper.extract_mentions_from_content(content)
            users = self.user_service.get_users_to_mention(users_mentioned)

            for mention_user in users:
                stmt = (
                    insert(MentionModel)
                    .values(
                        comment_id=comment_id,
                        mentioned_user_id=mention_user['id']
                    ) 
                )
                db.session.execute(stmt)
                db.session.commit()
                
            data = {
                "comment_id": comment_id,
                "content": content,
                "mentions": [user['name'] for user in users]
            }
            
            """ self.rabbit_service.publish("mention_comment_notification", data)
            self.rabbit_service.close() """
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo({'messerrorMsgage':  f'Error creating mentioned {str(e)}'})
            return {'message': f'Error creating mentioned: {str(e)}'}, 500
        
    def list_comments_to_users(self, user_id):
        try:
            stmt =  (
                select(
                    CommentModel.id.label('comment_id'),
                    CommentModel.content.label('comment_content'),
                    CommentModel.created_at,
                    CommentModel.updated_at
                )
                .select_from(MentionModel)
                .join(CommentModel, MentionModel.comment_id == CommentModel.id)
                .where(MentionModel.mentioned_user_id == user_id)
                .group_by(
                    CommentModel.id,
                    CommentModel.content,
                    CommentModel.created_at,
                    CommentModel.updated_at
                )
            )
            
            result = db.session.execute(stmt).all()
            if len(result) <= 0:
                return {"message": "Not mention found"}, 404
            
            mention_dict = []
            for row in result:
                comment_dict = {
                    "comment_id": row.comment_id,
                    "comment_content": row.comment_content,
                    "created_at": helper.formatting_time(row.created_at,"%Y-%m-%d %H:%M:%S"),
                    "updated_at": helper.formatting_time(row.updated_at,"%Y-%m-%d %H:%M:%S")
                }
                
                mention_dict.append(comment_dict)
                
            return {
                "message": "List of comments of a post", 
                "mentioned_comment": mention_dict
            } , 200
            
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo({'messerrorMsgage':  f'list_comments_to_users {str(e)}'})
            return {'message': f'list_comments_to_users: {str(e)}'}, 500