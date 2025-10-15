from connection import db
from utils.helpers import Helper
from logger.logging import LoggerApp
from models.user_model import UserModel
from sqlalchemy import select, insert, delete, update
from models.interesting_model import InterestingModel

class InterestingService:
    def __init__(self):
        self.helper = Helper()
        self.logger = LoggerApp()
        
    def createInteresting(self, interestingBody, user_id):
        if not interestingBody or 'interest_name' not in interestingBody:
            return {'message': 'Interest name and user_id required'}, 400 
         
        try:    
            stmt = (
                insert(InterestingModel).values(
                    interest_name=interestingBody['interest_name'], 
                    description=interestingBody.get('description', None), 
                    user_id=user_id
                )
                .returning(InterestingModel)
            )
        
            result = db.session.execute(stmt).fetchone()
            db.session.commit()       
            new_interest = result[0]
            
            return {
                'message': 'Interesting created', 
                'interesting': {
                    "id": new_interest.id,
                    "interest_name": new_interest.interest_name,
                    "description": new_interest.description,
                    "user_id": new_interest.user_id,
                    "created_at": self.helper.formatting_time(new_interest.created_at, "%Y-%m-%d %H:%M:%S"),
                    "updated_at": self.helper.formatting_time(new_interest.updated_at, "%Y-%m-%d %H:%M:%S")
                }
            }, 201
        except Exception as e:
            db.session.rollback() 
            return {'message': f'Error creating interesting: {str(e)}'}, 500
        
    def listingUserInterestings(self, user_id):
        try:
            stmt = (
                select(InterestingModel.interest_name)
                .where(InterestingModel.user_id == user_id)
                .order_by(InterestingModel.created_at.desc())
            )
            
            result = db.session.execute(stmt).all()            
            interest_dict = []
            for row in result:
                interest_item = {"interest_name": row.interest_name }
                interest_dict.append(interest_item)
                
            return interest_dict
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error listingUserInterestings: {str(e)}")
            return {'message': f'Error listing interestings: {str(e)}'}, 500
        
    def listingUsersSameInterest(self, current_user_id):
        try:
            subs_time = self.helper.formatting_time("", "%Y-%m-%d %H:%M:%S", "subs_time")
            current_user_interests_stmt = self.listingUserInterestings(current_user_id)
            stmt = (
                select(UserModel.id, UserModel.nick_name)
                .select_from(InterestingModel)
                .join(UserModel, InterestingModel.user_id == UserModel.id)
                .where(InterestingModel.user_id != current_user_id)
                .where(db.func.date(InterestingModel.created_at) >= subs_time)
                .where(InterestingModel.interest_name.in_([interest['interest_name'] for interest in current_user_interests_stmt]))
                .group_by(UserModel.id)
                .distinct(UserModel.id, UserModel.nick_name)
            )
            
            user_same_interest_dict = []
            result = db.session.execute(stmt).all()
            for row in result:
                user_dict = {
                    "user_id": row.id,
                    "nick_name": row.nick_name
                }
                
                user_same_interest_dict.append(user_dict)
            
            return user_same_interest_dict
        except Exception as e:
            db.session.rollback() 
            self.logger.logErrorInfo(f"Error listingUsersSameInterest: {str(e)}")