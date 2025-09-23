from connection import db
from flask import jsonify
from utils.helpers import Helper
from logger.logging import LoggerApp
from sqlalchemy import insert, select
from services.user_service import UserService
from models.mentions_model import MentionModel
from services.rabbit_mq_service import RabbitMqService

helper = Helper()

class MentionService:
    def __init__(self):
        self.logger = LoggerApp()
        self.user_service = UserService()
        self.rabbit_service = RabbitMqService()
        
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
            
            self.rabbit_service.publish("mention_comment_notification", data)
            self.rabbit_service.close()
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo({'messerrorMsgage':  f'Error creating mentioned {str(e)}'})
            return {'message': f'Error creating mentioned: {str(e)}'}, 500
        
            
        
        