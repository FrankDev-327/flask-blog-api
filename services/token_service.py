from connection import db  
from logger.logging import LoggerApp
from models.token_model import TokenModel

class TokenService:
    def __init__(self):
        self.logger = LoggerApp()
        self.token_model = TokenModel

    def createToken(self, tokenGenerated, marked_as_used=False):        
        new_token = self.token_model(token=tokenGenerated, marked_as_used=marked_as_used)
        try:
            db.session.add(new_token)
            db.session.commit()       
        except Exception as e:
            db.session.rollback()  
            self.logger.logErrorInfo({'message':  'Error creating token'})
            return {'message': f'Error creating token: {str(e)}'}, 500

    def getTokenById(self, tokenGenerated):
        token = self.token_model.query.filter_by(token=tokenGenerated).first()
        if token:
            return token.to_dict()
        return None