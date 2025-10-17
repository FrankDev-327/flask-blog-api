import os
from flask_restful import Resource, request
from werkzeug.utils import secure_filename
from middleware.check_token import require_token
from services.upload_files_service import UploadFileService
from middleware.check_image_extention import check_file_extension


class UploadFilesController(Resource):
    def __init__(self):
        super().__init__()
        self.uploadFileService = UploadFileService()

    @require_token
    @check_file_extension
    def post(self):
        try:
            file = request.files["file"]
            filename = secure_filename(file.filename)
            sizeFile = os.fstat(file.fileno()).st_size
            return self.uploadFileService.upload_image(filename, file, sizeFile)
        except Exception as e:
            return {"message": e}, 500
