from connection import db
from sqlalchemy import insert
from utils.helpers import Helper
from logger.logging import LoggerApp
from models.images_model import ImagesModel


class ImagesService:
    def __init__(self):
        self.helper = Helper()
        self.logger = LoggerApp()

    def insert_post_image(self, imageBody):
        try:
            stmt = insert(ImagesModel).values().returning(ImagesModel)

            result = db.session.execute(stmt)
            row = result.fetchone()
            db.session.commit()
            new_post_image = row[0]

            return True
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(f"Error insert_post_image: {str(e)}")
            return {"message": f"Error insert_post_image: {str(e)}"}, 500
