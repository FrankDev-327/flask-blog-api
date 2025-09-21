from flask import request
from flask_restful import Resource
from middleware.check_token import require_token
from services.post_service import PostService

class PostListController(Resource):    
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
    
    @require_token
    def get(self):
        """
        Get a list of posts
        ---
        tags:
          - Post
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
            description: List of posts with pagination
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
                      created_at:
                        type: string
                        format: date-time
                      updated_at:
                        type: string
                        format: date-time
                pagination:
                  type: object
                  properties:
                    page:
                      type: integer
                      example: 1
                    per_page:
                      type: integer
                      example: 10
                    total_posts:
                      type: integer
                      example: 25
                    total_pages:
                      type: integer
                      example: 3
        """
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        return self.post_service.getAllPosts(page, per_page)
