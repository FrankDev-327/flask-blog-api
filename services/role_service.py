import json
from connection import db 
from logger.logging import LoggerApp
from models.role_model import RoleModel

class RoleService:
    def __init__(self):
        self.logger = LoggerApp()   
        self.role_model = RoleModel
        
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
    
    def removeRoleFromUser(self, roleBody):
        if not roleBody or 'role_name'  not in roleBody or 'user_id' not in roleBody:
            self.logger.logErrorInfo({'message': 'Role name and user ID required'})
            return {'message': 'Role name and user ID required'}, 400  
        
        try:
            role = self.role_model.query.filter_by(role_name=roleBody['role_name'], user_id=roleBody['user_id']).first()
            if not role:
                self.logger.logErrorInfo({'message': 'Role not found for the user'})
                return {'message': 'Role not found for the user'}, 404
            
            db.session.delete(role)
            db.session.commit()       
            return {'message': 'Role removed from user'}, 200
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'message':  'Error removing role from user'})
            return {'message': f'Error removing role from user: {str(e)}'}, 500
        
    def updateRoleFromUser(self, role_id, roleBody):
        if not roleBody or 'role_name'  not in roleBody:
            self.logger.logErrorInfo({'message': 'Role name required'})
            return {'message': 'Role name required'}, 400  
        
        try:
            role = self.role_model.query.get(role_id)
            if not role:
                self.logger.logErrorInfo({'message': 'Role not found'})
                return {'message': 'Role not found'}, 404
            
            role.role_name = roleBody['role_name']
            db.session.commit()       
            return {'message': 'Role updated', 'role': role.to_dict()}, 200
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'message':  'Error updating role'})
            return {'message': f'Error updating role: {str(e)}'}, 500
        
    