from flask import jsonify
from connection import db  
from logger.logging import LoggerApp
from models.user_model import UserModel # Importing the db instance from connection.py


class UserService:
    def __init__(self):
        self.user_model = UserModel
        self.logger = LoggerApp

    def getUserById(self, user_id):
        user = self.user_model.query.get(user_id)
        if user:
            return {'id': user.id, 'name': user.name, 'email': user.email}, 200
        return {'message': 'User not found'}, 404

    def existUser(self, name):
        user = self.user_model.query.filter_by(name=name).first()
        if user:
            return True
        return None
    
    def getAllUsers(self):
        users = self.user_model.query.all()
        return [{'id': user.id, 'name': user.name, 'email': user.email} for user in users], 200

    def createUser(self, userBody):
        print(userBody['name'])
        # Logic to create a new user
        if not userBody or 'name' not in userBody or 'email' not in userBody:
            return {'message': 'Name and email required'}, 400  
        
        #userExist = self.existUser(userBody['name'])
        #if userExist:
        #    return {'message': 'User exists'}, 404
        
        new_user = self.user_model(name=userBody['name'], email=userBody['email'])
        try:
            db.session.add(new_user)  # Add to DB session
            db.session.commit()       # Commit changes
            return {'message': 'User created', 'user': new_user.to_dict()}, 201
        except Exception as e:
            db.session.rollback()     # Rollback on error
            self.logger.logInfo(e)
            return {'message': f'Error creating user: {str(e)}'}, 500

    def put(self, user_id):
        # Logic to update an existing user
        return {'message': 'User updated', 'user_id': user_id}, 200

    def delete(self, user_id):
        # Logic to delete a user
        return {'message': 'User deleted', 'user_id': user_id}, 204
