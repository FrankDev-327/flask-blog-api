from connection import db
from flask import jsonify
from utils.helpers import Helper
from logger.logging import LoggerApp
from sqlalchemy import insert, select
from models.notifications_model import NotificationModel

class NotificationService:
    def __init__(self):
        self.helper = Helper()
        self.logger = LoggerApp()
        
    def create_notification(self, notification_body):
        try:
            bulk_insert = []
            for user_id in notification_body['user_mentioned_ids']:
                notification_to_insert = NotificationModel(
                    user_mentioned_id=user_id,
                    comment_id=notification_body['comment_id'],
                    type_notification=notification_body['type_notification'],
                    notification_preview=notification_body['notification_preview'][1:30],
                )
                bulk_insert.append(notification_to_insert)
  
            db.session.bulk_save_objects(bulk_insert)
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error create_notification: {str(e)}")
            
    def list_user_notifications(self):
        try:
            pass
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error list_user_notifications: {str(e)}")