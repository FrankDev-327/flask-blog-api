from connection import db
from logger.logging import LoggerApp
from models.role_model import RoleModel
from sqlalchemy import insert, select, delete


class RoleService:
    def __init__(self):
        self.logger = LoggerApp()
        self.role_model = RoleModel

    def assignRoToUser(self, roleBody):
        if not roleBody or "role_name" not in roleBody or "user_id" not in roleBody:
            self.logger.logErrorInfo({"message": "Role name required"})
            return {"message": "Role name required"}, 400

        existRole = self._checkUserHasRole(roleBody)
        if existRole:
            return {"message": "User was already assigned to this role"}, 400

        try:
            stmt = (
                insert(RoleModel)
                .values(role_name=roleBody["role_name"], user_id=roleBody["user_id"])
                .returning(RoleModel)
            )

            result = db.session.execute(stmt)
            row = result.fetchone()
            db.session.commit()
            role_assigned = row[0]

            return {
                "message": "Role created",
                "role": {
                    "id": role_assigned.id,
                    "role_name": role_assigned.role_name,
                    "user_id": role_assigned.user_id,
                },
            }, 201
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"message": "Error creating role"})
            return {"message": f"Error creating role: {str(e)}"}, 500

    def _checkUserHasRole(self, roleBody):
        try:
            stmt = (
                select(RoleModel)
                .where(RoleModel.user_id == roleBody["user_id"])
                .where(RoleModel.role_name == roleBody["role_name"])
            )
            roleUser = db.session.execute(stmt).scalar_one_or_none()
            if roleUser:
                return True
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"message": "Error creating role"})
            return {"message": f"Error creating role: {str(e)}"}, 500

    def removeRoleFromUser(self, roleBody):
        if not roleBody or "role_name" not in roleBody or "user_id" not in roleBody:
            self.logger.logErrorInfo({"message": "Role name and user ID required"})
            return {"message": "Role name and user ID required"}, 400

        try:
            existRole = self._checkUserHasRole(roleBody)
            if not existRole:
                return {"message": "Ths user does not have any role assigned"}, 400

            stmt = (
                delete(RoleModel)
                .where(RoleModel.user_id == roleBody["user_id"])
                .where(RoleModel.role_name == roleBody["role_name"])
                .returning(RoleModel)
            )

            db.session.execute(stmt)
            db.session.commit()
            return {"message": "Role for the user was deleted"}, 201
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"message": "Error removing role from user"})
            return {"message": f"Error removing role from user: {str(e)}"}, 500
