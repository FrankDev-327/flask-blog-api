import os
import cloudinary
from logger.logging import LoggerApp
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


class UploadFileService:
    def __init__(self):
        self.logger = LoggerApp()
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_SECRET_API_KEY"),
            secure=True,
        )

    def upload_image(
        self,
        file_data,
        file_size=0,
        filename="",
    ):
        try:
            upload_result = upload(file_data)
            image_url, _ = cloudinary_url(upload_result["public_id"], crop="fill")

            return {"url": image_url, "public_id": upload_result["public_id"]}

        except Exception as exc:
            # Always convert the exception to string for safe JSON response
            self.logger.logErrorInfo(f"Upload failed: {exc}")
            return {"message": str(exc)}, 500
