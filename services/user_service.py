from utils.helpers import Helper
from connection import db
from sqlalchemy import select, insert, delete
from logger.logging import LoggerApp
from models.user_model import UserModel
from models.role_model import RoleModel


class UserService:
    def __init__(self):
        self.helper = Helper()
        self.logger = LoggerApp()

    def get_users_to_mention(self, users_from_content):
        try:
            stmt = select(UserModel.id, UserModel.name).where(
                UserModel.name.in_(users_from_content)
            )
            users = db.session.execute(stmt).all()
            users_mentioned = [{"id": user.id, "name": user.name} for user in users]

            return users_mentioned
        except Exception as e:
            self.logger.logErrorInfo({"getUserByIdOrAll ": str(e)})
            return {"message": f"Error retrieving user: {str(e)}"}, 500

    def getAllUsers(self):
        stmt = select(UserModel)
        users = db.session.execute(stmt).scalars().all()

        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email,
            }

            user_list.append(user_dict)
        return user_list, 200

    def getUserByIdOrAll(self, user_id):
        try:
            if user_id:
                stmt = select(UserModel).where(UserModel.id == user_id)
                user = db.session.execute(stmt).scalar_one_or_none()
                if not user:
                    return {"message": "User not found"}, 404
                user_dict = {
                    "id": user.id,
                    "name": user.name,
                    "nick_name": user.nick_name,
                    "email": user.email,
                }
                return user_dict, 200
            else:
                return {"message": "User ID is required"}, 400
        except Exception as e:
            self.logger.logErrorInfo({"getUserByIdOrAll ": str(e)})
            return {"message": f"Error retrieving user: {str(e)}"}, 500

    def existUser(self, name):
        stmt = select(UserModel).where(UserModel.name == name)
        user = db.session.execute(stmt).scalar_one_or_none()
        if user:
            return True
        return None

    def checkExistinUser(self, userBody):
        try:
            stmt = (
                select(UserModel, RoleModel)
                .join(RoleModel, UserModel.id == RoleModel.user_id)
                .where(UserModel.nick_name == userBody["nick_name"])
            )

            row = db.session.execute(stmt).fetchone()
            if row is None:
                return {"message": "user not found or wrong password"}, 404

            user, role = row
            comparePassword = self.helper.compareHashAndPlainText(
                userBody["password"], user.password
            )

            if not comparePassword:
                return {"message": "user not found or wrong password"}, 404

            userData = {
                "id": user.id,
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email,
                "roles": role.role_name,
            }

            return userData, 200
        except Exception as e:
            self.logger.logErrorInfo({"checkExistinUser": str(e)})
            return {"message": f"Error checking user info: {str(e)}"}, 500

    def createUser(self, userBody):
        if not userBody or "name" not in userBody or "email" not in userBody:
            self.logger.logErrorInfo({"createUser": "Name and email required"})
            return {"message": "Name and email required"}, 400

        try:
            if self.existUser(userBody["name"]):
                return {"message": "User already exists"}, 409

            new_user = insert(UserModel).values(
                name=userBody["name"],
                email=userBody["email"],
                password=self.helper.hashingTextToHash(userBody["password"]),
                nick_name=userBody["nick_name"],
            )
            db.session.execute(new_user).first()
            db.session.commit()

            return {"message": "User created"}, 201
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"createUser": str(e)})
            return {"message": f"Error creating user: {str(e)}"}, 500

    def put(self, user_id):
        return {"message": "User updated", "user_id": user_id}, 200

    def delete_user(self, user_body):
        try:
            stmt = (
                delete(UserModel)
                .where(UserModel.name == user_body["name"])
                .where(UserModel.nick_name == user_body["nick_name"])
                .returning(UserModel)
            )

            db.session.execute(stmt)
            db.session.commit()
            return {"message": "User was deleted"}, 201
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"delete user": str(e)})
            return {"message": f"Error deleting user: {str(e)}"}, 500
