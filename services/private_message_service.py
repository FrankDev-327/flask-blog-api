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

    def get_private_message_by_id(self, sender_id, receiver_id, page, per_page):
        try:
            stmt = (
                    select(PrivateMessageModel).where(
                        PrivateMessageModel.sender_id == sender_id
                    )
                    .where(PrivateMessageModel.receiver_id == receiver_id)
                    .limit(per_page)
                    .offset((page - 1) * per_page)
                    .order_by(PrivateMessageModel.created_message_at.desc())
                )
            
            total_messages = db.session.execute(select(db.func.count()).select_from(PrivateMessageModel)).scalar_one()
            total_pages = (total_messages + per_page - 1)
            
            result = db.session.execute(stmt).scalars().all()
            messages_list = [ 
                {
                    "id": message.id,
                    "content": message.content,
                    "sender_id": message.sender_id,
                    "receiver_id": message.receiver_id,
                    "created_at": self.helper.formatting_time(message.created_message_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": self.helper.formatting_time(message.updated_message_at, "%Y-%m-%d %H:%M:%S")
                } for message in result
            ] 
            
            return {'private_message': messages_list, "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total_comments": total_messages,
                    "total_pages": total_pages
                }}, 200
        except Exception as e:
            self.logger.error(f'Error sending private message: {str(e)}')
            return {'message': f'Error retrieving private messages: {str(e)}'}, 500.
         