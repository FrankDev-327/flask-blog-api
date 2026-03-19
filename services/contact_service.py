from connection import db
from flask_restful import request
from utils.helpers import Helper
from logger.logging import LoggerApp
from models.contacts_model import ContactsModel
from redis_serve.redis_service import RedisService
from sqlalchemy import select, insert


class ContactService:
    def __init__(self):
        self.helper = Helper()
        self.logger = LoggerApp()
        self.redis_service = RedisService()

    def add_contact(self, user_id, contact_id):
        if not contact_id:
            return {"message": "contact_id are required"}, 400

        try:
            existing_contact = self.__check_contact_exists(user_id, contact_id)
            if existing_contact:
                return {"message": "Contact already exists"}, 400

            stmt = (
                insert(ContactsModel)
                .values(user_id=user_id, contact_id=contact_id)
                .returning(ContactsModel)
            )

            result = db.session.execute(stmt).fetchone()
            db.session.commit()
            new_contact = result[0]
            nick_name = request.user["nick_name"]
            notify_user_request = {
                "request_id": new_contact.id,
                "contact_id": contact_id,
                "type": "friend_request_notification",
                "content": f"You have a new contact request from: {nick_name}",
            }

            self.redis_service.publish(
                "friend_request_notification", notify_user_request
            )
            return {
                "message": "Contact request sent",
                "contact": {
                    "id": new_contact.id,
                    "user_id": new_contact.user_id,
                    "contact_id": new_contact.contact_id,
                    "status": new_contact.status,
                    "created_at": self.helper.formatting_time(
                        new_contact.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                },
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error adding contact: {str(e)}"}, 500

    def __check_contact_exists(self, user_id, contact_id):
        try:
            stmt = select(ContactsModel).where(
                ContactsModel.user_id == user_id, ContactsModel.contact_id == contact_id
            )

            return db.session.execute(stmt).scalar_one_or_none()
        except Exception as e:
            self.logger.logErrorInfo(f"Error checking contact existence: {str(e)}")
            raise

    def get_contacts(self, user_id):
        if not user_id:
            return {"message": "user_id is required"}, 400

        try:
            stmt = select(ContactsModel).where(ContactsModel.user_id == user_id)
            result = db.session.execute(stmt)
            contacts = result.scalars().all()

            contacts_list = [
                {
                    "id": contact.id,
                    "user_id": contact.user_id,
                    "contact_id": contact.contact_id,
                    "status": contact.status,
                    "created_at": self.helper.formatting_time(
                        contact.created_at, "%Y-%m-%d %H:%M:%S"
                    ),
                }
                for contact in contacts
            ]

            return {"contacts": contacts_list}, 200
        except Exception as e:
            return {"message": f"Error retrieving contacts: {str(e)}"}, 500
