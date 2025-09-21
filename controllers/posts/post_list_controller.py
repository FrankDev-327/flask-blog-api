from base_resource import BaseResource
from flask import request
from middleware.check_token import require_token
from services.post_service import PostService

class PostListController(BaseResource):
    method_map = {'GET': 'getAllPosts'}
    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
    
    @require_token
    def getAllPosts(self):
        """
        Get a list of posts
        ---
        parameters:
          - name: page
            in: query
            type: integer
            required: false
            default: 1
          - name: per_page
            in: query
            type: integer
            required: false
            default: 10
        responses:
          200:
            description: List of posts
            schema:
              type: object
              properties:
                message:
                  type: string
                posts:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      content:
                        type: string
        """
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        return self.post_service.getAllPosts(page, per_page)
