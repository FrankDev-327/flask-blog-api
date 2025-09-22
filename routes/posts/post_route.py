from flask_restful import Api
from controllers.posts.post_list_comment import PostListComments
from controllers.posts.post_controller import PostCreateController
from controllers.posts.post_list_controller import PostListController
from controllers.posts.post_update_controller import PostUpdateController
from controllers.posts.post_get_details_controller import PostGetDetailsController
from controllers.posts.post_seacht_by_title_controller import PostGetSearchTitleController

def register_post_routes(api: Api):
    api.add_resource(PostListController, '/post', endpoint='post_all')
    api.add_resource(PostCreateController, '/post', endpoint='post_create')
    api.add_resource(PostUpdateController, '/post/<int:post_id>', endpoint='post_update')
    api.add_resource(PostGetSearchTitleController, '/post/search', endpoint='post_title_search')
    api.add_resource(PostGetDetailsController, '/post/<int:post_id>', endpoint='post_get_details')
    api.add_resource(PostListComments, '/post/<int:post_id>/comments', endpoint='post_list_comments')