from flask_restful import Api
from controllers.upload_files.upload_fiiles_controller import UploadFilesController


def register_upload_files_route(api: Api):
    api.add_resource(
        UploadFilesController, "/upload", methods=["POST"], endpoint="upload_files"
    )
