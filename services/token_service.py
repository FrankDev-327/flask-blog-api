from connection import db
from logger.logging import LoggerApp
from sqlalchemy import insert, select
from models.token_model import TokenModel


class TokenService:
    def __init__(self):
        self.logger = LoggerApp()
        self.token_model = TokenModel

    def createToken(self, tokenGenerated, marked_as_used=False):
        try:
            stmt = insert(TokenModel).values(
                token=tokenGenerated, marked_as_used=marked_as_used
            )

            db.session.execute(stmt)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo({"message": "Error creating token"})
            return {"message": f"Error creating token: {str(e)}"}, 500

    def getTokenById(self, tokenGenerated):
        stmt = select(TokenModel.token).where(TokenModel.token == tokenGenerated)
        token_info = db.session.execute(stmt).scalar_one_or_none()
        if token_info:
            return {"token": token_info}
        return None
