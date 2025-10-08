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
        
    def create_notification(self, user_id, comment_id, type_notification, notification_preview):
        try:
            print(notification_preview)
            stmt = (
                insert(NotificationModel)
                .values(
                    user_mentioned_id=user_id,
                    comment_id=comment_id,
                    type_notification=type_notification,
                    notification_preview=notification_preview[1:30],
                )
            )
            
            db.session.execute(stmt)
            db.session.commit()
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error create_notification: {str(e)}")
            
    def list_user_notifications(self, user_id):
        try:
            subs_time = self.helper.formatting_time("", "%Y-%m-%d %H:%M:%S", "subs_time")
            stmt = (
                select(
                    NotificationModel.comment_id,
                    NotificationModel.created_at,
                    NotificationModel.type_notification,
                    NotificationModel.notification_preview,
                    )
                .where(NotificationModel.user_mentioned_id==user_id)
                .where(db.func.date(NotificationModel.created_at) >= subs_time)
                .distinct(NotificationModel.comment_id)
            )
   
            notitications = db.session.execute(stmt).all()
            notification_dict = [
                {
                    "comment_id": notification.comment_id,
                    "type_notification": notification.type_notification,
                    "notification_preview": notification.notification_preview,
                    "created_at": self.helper.formatting_time(notification.created_at, "%Y-%m-%d %H:%M:%S"),
                }
                for notification in notitications
            ]
            
            return {
                "message": "List of notifications",
                "notifications": notification_dict
            }, 200
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error list_user_notifications: {str(e)}")