from utils.helpers import Helper
from flask import jsonify
from connection import db  
from sqlalchemy import select, join, insert
from queries.session_query import Query
from logger.logging import LoggerApp
from models.user_model import UserModel 
from models.role_model import RoleModel

class UserService:
    def __init__(self):
        self.helper = Helper()
        self.queries = Query()
        self.logger = LoggerApp()
        self.user_model = UserModel

    def getAllUsers(self):
        stmt = select(UserModel)
        users = db.session.execute(stmt).scalars().all()

        user_list = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "nick_name": user.nick_name,
                "email": user.email
            }
            
            user_list.append(user_dict)
        return user_list, 200

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
            stmt = (
                select(UserModel, RoleModel)
                .join(RoleModel, UserModel.id == RoleModel.user_id)
                .where(UserModel.nick_name == userBody['nick_name'])
            )

            row = db.session.execute(stmt).fetchone()
            if row is None:
                return {'message': 'user not found or wrong password'}, 404

            user, role = row  
            comparePassword = self.helper.compareHashAndPlainText(
                userBody['password'], user.password
            )
            if not comparePassword:
                return {'message': 'user not found or wrong password'}, 404

        except Exception as e: 
            self.logger.logErrorInfo({'userError': str(e)})
            return {'message': f'Error checking user info: {str(e)}'}, 500

        userData = {
            "id": user.id,
            "name": user.name,
            "nick_name": user.nick_name,
            "email": user.email,
            "roles": role.role_name, 
        }
        
        return userData, 200
    
    def createUser(self, userBody):
        if not userBody or 'name' not in userBody or 'email' not in userBody:
            self.logger.logErrorInfo({'errorMsg':'Name and email required'})
            return {'message': 'Name and email required'}, 400
        
        try:
            new_user = insert(UserModel).values(
                name=userBody['name'], 
                email=userBody['email'], 
                password= self.helper.hashingTextToHash(userBody['password']),          
                nick_name=userBody['nick_name']
            )
            db.session.execute(new_user).first()
            db.session.commit()
            
            """
            new_user = self.user_model(
                name=userBody['name'], 
                email=userBody['email'], 
                password= self.helper.hashingTextToHash(userBody['password']),
                nick_name=userBody['nick_name']
            )
            
            db.session.add(new_user)  
            db.session.commit()  
            """   
               
            return {'message': 'User created', 'user': new_user}, 201
        
        except Exception as e:
            db.session.rollback()     
            self.logger.logErrorInfo({'errorMsg':str(e)})
            return {'message': f'Error creating user: {str(e)}'}, 500

    def put(self, user_id):
        return {'message': 'User updated', 'user_id': user_id}, 200

    def delete(self, user_id):
        return {'message': 'User deleted', 'user_id': user_id}, 204
