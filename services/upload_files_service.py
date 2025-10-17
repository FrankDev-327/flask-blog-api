import os
from minio import Minio
from minio.error import S3Error
from logger.logging import LoggerApp


class UploadFileService:
    def __init__(self):
        self.logger = LoggerApp()
        self.minio_client = Minio(
            os.getenv("FIELD_HUB_BUCKET_URL"),
            os.getenv("FIELD_HUB_BUCKET_ACCESS_KEY"),
            os.getenv("FIELD_HUB_BUCKET_SECRET_KEY"),
            secure=True
        )

    def upload_image(self, filename, data, length):
        try:
            fileStored = self.minio_client.put_object(
                os.getenv("FIELD_HUB_BUCKET_NAME"), filename, data, length
            )

            return fileStored
        except S3Error as exc:
            self.logger.logErrorInfo(
                f"Something went wrong uploading a file: {exc.message}"
            )
            return {"message": exc.message}, 500
