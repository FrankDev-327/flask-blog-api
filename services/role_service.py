import json
from connection import db 
from logger.logging import LoggerApp
from models.role_model import RoleModel
from middleware.check_token import require_token, check_user_role

class RoleService:
    def __init__(self):
        self.logger = LoggerApp()   
        self.role_model = RoleModel
        
    @require_token
    @check_user_role
    def assignRoToUser(self, roleBody):
        if not roleBody or 'role_name'  not in roleBody or 'user_id' not in roleBody:
            self.logger.logErrorInfo({'message': 'Role name required'})
            return {'message': 'Role name required'}, 400  
        
        new_role = self.role_model(role_name=roleBody['role_name'], user_id=roleBody['user_id'])
        try:
            db.session.add(new_role)
            db.session.commit()       
            return {'message': 'Role created', 'role': new_role.to_dict()}, 201
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'message':  'Error creating role'})
            return {'message': f'Error creating role: {str(e)}'}, 500
        