from sqlalchemy import select, join
from models.user_model import UserModel
from models.role_model import RoleModel
from connection import db
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
            
            rows = db.session.execute(stmt).first()
            if not rows:
                self.logger.logErrorInfo({'message': 'User not found'})
                return None

            if rows:
                user, role = rows
                user_data = {
                    "id": user.id,
                    "name": user.name,
                    "nick_name": user.nick_name,
                    "email": user.email,
                    "roles": role.role_name  # just one role here
                }
            print(user_data)
            return user_data

        except Exception as e:
            self.logger.logErrorInfo(f"Error fetching user with roles: {e}")
            return None