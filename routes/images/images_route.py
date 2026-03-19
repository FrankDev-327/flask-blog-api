from flask_restful import Api
from controllers.images.insert_image_to_post_controller import (
    InsertImageToPostController,
)


def register_images_router(api: Api):
    api.add_resource(
        InsertImageToPostController,
        "/images",
        methods=["POST"],
        endpoint="images_create",
    )
