from flask_restful import request, Resource
from middleware.check_token import require_token
from services.post_service import PostService

class PostListComments(Resource): 
    def __init__(self):
        super().__init__()
        self.post_service = PostService()
        
    @require_token
    def get(self, post_id):
        """
        List all comments of a specific post
        ---
        tags:
          - Post
        parameters:
          - name: post_id
            in: path
            type: integer
            required: true
            description: ID of the post to retrieve comments for
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
            description: List of comments with pagination
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "List of comments of a post"
                post:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    title:
                      type: string
                      example: "test_post_100000000"
                    comments:
                      type: array
                      items:
                        type: object
                        properties:
                          id:
                            type: integer
                            example: 1
                          content:
                            type: string
                            example: "test_content_4"
                          created_at:
                            type: string
                            format: date-time
                            example: "2025-08-30 20:40:12"
                          updated_at:
                            type: string
                            format: date-time
                            example: "2025-08-30 20:40:12"
                pagination:
                  type: object
                  properties:
                    page:
                      type: integer
                      example: 1
                    per_page:
                      type: integer
                      example: 2
                    total_comments:
                      type: integer
                      example: 7
                    total_pages:
                      type: integer
                      example: 8
          404:
            description: Post not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post not found"
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        return self.post_service.listAllCommentByPostId(post_id, page, per_page)
