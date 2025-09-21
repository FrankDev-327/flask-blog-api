from flask_restful import Api
from controllers.authentication.comment_controller import CommentController
from controllers.comments.comment_update_controller import CommentUpdateController
from controllers.comments.comment_get_details_controller import CommentGetDetailsController

def register_comment_route(api: Api):
    api.add_resource(CommentController, '/comments', methods=['POST'], endpoint='comments')  
    api.add_resource(CommentUpdateController, '/comments/<int:comment_id>', methods=['PUT'], endpoint='comments_update') 
    api.add_resource(CommentGetDetailsController, '/comments/<int:comment_id>', methods=['GET'], endpoint='comments_details')  
