from utils.helpers import Helper
from flask import jsonify
from connection import db  
from queries.session_query import Query
from middleware.check_token import require_token
from logger.logging import LoggerApp
from models.user_model import UserModel 

class UserService:
    def __init__(self):
        self.helper = Helper()
        self.queries = Query()
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
        return 
    
    def checkExistinUser(self, userBody):
        try:
            userInfo = self.user_model.query.filter_by(nick_name=userBody['nick_name']).first()
            if  userInfo is None:
                return {'messgae':'user not found not wrong passwor'}, 404
            
            data = self.queries.getUserWithRoles(3)
            #print(data)
            userInfo = userInfo.to_dict(include_relationships=True)
            comparePassword = self.helper.compareHashAndPlainText( userBody['password'], userInfo['password'])
            if not comparePassword:
                return {'messgae':'user not found not wrong passwor'}, 404
            
        except Exception as e: 
            self.logger.logErrorInfo({'errorMsg':str(e)})
            return {'message': f'Error checking user info: {str(e)}'}, 500
        
        del userInfo['password']
        return {'user': userInfo, 'message': 'user auth'}, 200
    
    def createUser(self, userBody):
        if not userBody or 'name' not in userBody or 'email' not in userBody:
            self.logger.logErrorInfo({'errorMsg':'Name and email required'})
            return {'message': 'Name and email required'}, 400
        
        try:
            new_user = self.user_model(
                name=userBody['name'], 
                email=userBody['email'], 
                password= self.helper.hashingTextToHash(userBody['password']),
                nick_name=userBody['nick_name']
            )
            
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
