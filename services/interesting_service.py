from connection import db
from utils.helpers import Helper
from logger.logging import LoggerApp
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
