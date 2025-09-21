from flask_restful import Api
from controllers.posts.post_list_comment import PostListComments
from controllers.posts.post_controller import PostCreateController
from controllers.posts.post_list_controller import PostListController
from controllers.posts.post_update_controller import PostUpdateController
from controllers.posts.post_get_details_controller import PostGetDetailsController

def register_post_routes(api: Api):
    api.add_resource(PostListController, '/post', methods=['GET'], endpoint='post_all')
    api.add_resource(PostCreateController, '/post', methods=['POST'], endpoint='post_create')
    api.add_resource(PostUpdateController, '/post/<int:post_id>', methods=['PUT'], endpoint='post_update')
    api.add_resource(PostGetDetailsController, '/post/<int:post_id>', methods=['GET'], endpoint='post_get')
    api.add_resource(PostListComments, '/post/<int:post_id>/comments', methods=['GET'], endpoint='post_get_comments')