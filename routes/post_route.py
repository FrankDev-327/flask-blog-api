from flask_restful import Api
from controllers.post_controller import PostController

def register_post_routes(api: Api):
    api.add_resource(PostController, '/post', methods=['POST'], endpoint='post_create')
    api.add_resource(PostController, '/post', methods=['GET'], endpoint='post_all')
    api.add_resource(PostController, '/post/<int:post_id>', methods=['GET'], endpoint='post_get')