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
            stmt = (
                insert(ImagesModel)
                .values(
                    url_file=imageBody["url_file"],
                    ext_file=imageBody["ext_file"],
                    size_file=imageBody["size_file"],
                    public_id=imageBody["public_id"],
                    post_id=imageBody["post_id"],
                )
                .returning(ImagesModel)
            )

            result = db.session.execute(stmt)
            row = result.fetchone()
            db.session.commit()
            new_post_image = row[0]

            return {
                "message": "Upload successful",
                "url_file": new_post_image.url_file,
                "ext_file": new_post_image.ext_file,
                "size_file": new_post_image.size_file,
                "public_id": new_post_image.public_id,
                "post_id": new_post_image.post_id,
            }, 200
        except Exception as e:
            db.session.rollback()
            self.logger.logErrorInfo(f"Error insert_post_image: {str(e)}")
            return {"message": f"Error insert_post_image: {str(e)}"}, 500
