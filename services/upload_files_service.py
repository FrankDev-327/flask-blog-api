import os
from minio import Minio
from minio.error import S3Error
from logger.logging import LoggerApp


class UploadFileService:
    def __init__(self):
        self.logger = LoggerApp()
        self.minio_client = Minio(
            os.getenv("FIELD_HUB_BUCKET_URL_FLASK"),
            access_key=os.getenv("FIELD_HUB_BUCKET_ACCESS_KEY"),
            secret_key=os.getenv("FIELD_HUB_BUCKET_SECRET_KEY"),
            secure=False,
        )

    def upload_image(self, filename, file_data, file_size):
        try:
            result = self.minio_client.put_object(
                os.getenv("FIELD_HUB_BUCKET_NAME_FLASK"),
                filename,
                file_data,
                file_size
            )

            response = {
                "object_name": filename,
                "bucket": os.getenv("FIELD_HUB_BUCKET_NAME_FLASK"),
                "etag": str(result.etag),
                "version_id": str(result.version_id) if result.version_id else None,
            }

            print(response)  # for debug
            return response, 200

        except S3Error as exc:
            self.logger.logErrorInfo(f"Upload failed: {exc}")
            return {"message": str(exc)}, 500
