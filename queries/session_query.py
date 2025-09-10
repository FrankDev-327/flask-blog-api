from sqlalchemy import select, join
from models.user_model import UserModel
from models.role_model import RoleModel
from connection import db
#from sqlalchemy.orm import Session
from logger.logging import LoggerApp

class Query:
    def __init__(self):
        self.logger = LoggerApp()

    def getUserWithRoles(self, user_id):
        try:
            stmt = (
                select(UserModel, RoleModel)
                .join(RoleModel, UserModel.id == RoleModel.user_id)
                .where(UserModel.id == user_id)
            )
            rows = db.session.execute(stmt).all()

            if not rows:
                self.logger.logErrorInfo({'message': 'User not found'})
                return None

            user = rows[0][0]
            roles = [role.role_name for (_, role) in rows]

            user_data = {
                'id': user.id,
                'name': user.name,
                'nick_name': user.nick_name,
                'email': user.email,
                'roles': roles
            }
            return user_data

        except Exception as e:
            self.logger.error(f"Error fetching user with roles: {e}")
            return None