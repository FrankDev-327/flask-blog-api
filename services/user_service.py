from flask import jsonify
from connection import db  
from logger.logging import LoggerApp
from models.user_model import UserModel 

class UserService:
    def __init__(self):
        self.logger = LoggerApp()
        self.user_model = UserModel

    def getAllUsers(self):
        users = self.user_model.query.all()
        return [u.to_dict() for u in users], 200

    def getUserByIdOrAll(self, user_id):
        if user_id:
            user = self.user_model.query.get_or_404(user_id)
            return user.to_dict(include_relationships=True), 200            

    def existUser(self, name):
        user = self.user_model.query.filter_by(name=name).first()
        if user:
            return True
        return None
    
    def createUser(self, userBody):
        if not userBody or 'name' not in userBody or 'email' not in userBody:
            self.logger.logErrorInfo({'errorMsg':'Name and email required'})
            return {'message': 'Name and email required'}, 400
        
        try:
            new_user = self.user_model(name=userBody['name'], email=userBody['email'])
            db.session.add(new_user)  
            db.session.commit()       
            return {'message': 'User created', 'user': new_user.to_dict()}, 201
        
        except Exception as e:
            db.session.rollback()     
            self.logger.logErrorInfo({'errorMsg':str(e)})
            return {'message': f'Error creating user: {str(e)}'}, 500

    def put(self, user_id):
        return {'message': 'User updated', 'user_id': user_id}, 200

    def delete(self, user_id):
        return {'message': 'User deleted', 'user_id': user_id}, 204
