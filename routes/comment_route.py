from flask_restful import Api
from controllers.comment_controller import CommentController

def register_comment_route(api: Api):
    api.add_resource(CommentController, '/comments', methods=['POST'], endpoint='comments')  
    api.add_resource(CommentController, '/comments/<int:post_id>', methods=['GET'], endpoint='comments_post')
    api.add_resource(CommentController, '/comments/<int:comment_id>', methods=['PUT'], endpoint='comments_update')  
