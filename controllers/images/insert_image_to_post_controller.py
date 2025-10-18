import os
from werkzeug.utils import secure_filename
from flask_restful import Resource, request
from middleware.check_token import require_token
from services.images_service import ImagesService
from services.upload_files_service import UploadFileService
from middleware.check_image_extention import check_file_extension


class InsertImageToPostController(Resource):
    def __init__(self):
        super().__init__()
        self.imageService = ImagesService()
        self.uploadFileService = UploadFileService()

    @require_token
    @check_file_extension
    def post(self):
        """
        Upload an image and associate it with a post
        ---
        tags:
          - Images
        summary: Upload an image file to Cloudinary and link it to a post
        description: >
          Uploads an image to Cloudinary and associates it with a given post.
          The `post_id` must be provided as a query string parameter.
          Requires a valid Bearer token and a supported image file.
        security:
          - BearerAuth: []
        parameters:
          - name: post_id
            in: query
            type: integer
            required: true
            description: ID of the post to associate the uploaded image with
          - name: file
            in: formData
            type: file
            required: true
            description: Image file to upload
        consumes:
          - multipart/form-data
        produces:
          - application/json
        responses:
          200:
            description: Upload successful
            examples:
              application/json:
                message: Upload successful
                url_file: https://res.cloudinary.com/flaskapp/image/upload/c_fill/file_lqmvuc
                ext_file: ""
                size_file: 5591694
                public_id: file_lqmvuc
                post_id: 3
          400:
            description: Bad request - missing or invalid file
          401:
            description: Unauthorized - invalid or missing token
          500:
            description: Internal server error during upload
        """
        post_id = request.args.get("post_id")
        file = request.files["file"]
        filename = secure_filename(file.filename)
        sizeFile = os.fstat(file.fileno()).st_size
        imageUploaded = self.uploadFileService.upload_image(file, filename, sizeFile)

        imgInfo = {
            "url_file": imageUploaded["url"],
            "public_id": imageUploaded["public_id"],
            "ext_file": "",
            "size_file": sizeFile,
            "post_id": post_id,
        }

        return self.imageService.insert_post_image(imgInfo)
