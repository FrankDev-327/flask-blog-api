from connection import db
from utils.helpers import Helper
from logger.logging import LoggerApp
from sqlalchemy import select, insert, delete, update
from models.private_message_model import PrivateMessageModel

class PrivateMessageService:    
    def __init__(self):
        self.logger = LoggerApp()
        self.helper = Helper()
    
    def save_private_message(self, messageBody):         
        try:    
            stmt = (
                insert(PrivateMessageModel).values(
                    content=messageBody['content'], 
                    sender_id=messageBody['sender_id'], 
                    receiver_id=messageBody['receiver_id']
                )
            )
        
            db.session.execute(stmt)
            db.session.commit()       
            
        except Exception as e:
            db.session.rollback() 
            self.logger.error(f'Error saving private message: {str(e)}')

    def get_private_message_by_id(self, sender_id):
        try:
            stmt = (select(PrivateMessageModel).where(PrivateMessageModel.sender_id == sender_id))
            result = db.session.execute(stmt).all()
    
            return {
                'private_message': [ {
                    "id": message.id,
                    "content": message.content,
                    "sender_id": message.sender_id,
                    "receiver_id": message.receiver_id,
                    "created_at": self.helper.formatting_time(message.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": self.helper.formatting_time(message.updated_at, "%Y-%m-%d %H:%M:%S")
                } ] for message in result
            }, 200
        except Exception as e:
            self.logger.error(f'Error sending private message: {str(e)}')
            return {'message': f'Error retrieving private messages: {str(e)}'}, 500.
         