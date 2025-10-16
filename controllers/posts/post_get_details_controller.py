from flask_restful import Resource
from middleware.check_token import require_token
from services.post_service import PostService


class PostGetDetailsController(Resource):
    def __init__(self):
        super().__init__()
        self.post_service = PostService()

    @require_token
    def get(self, post_id):
        """
        Get details of a specific post
        ---
        tags:
          - Post
        parameters:
          - name: post_id
            in: path
            type: integer
            required: true
            description: ID of the post to retrieve
        responses:
          200:
            description: Post details
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 20
                title:
                  type: string
                  example: "test_post_1"
                content:
                  type: string
                  example: "jerioth se bebia mi semen por el ano y a veces se lo echaba en la cara o se lo tragaba toda la leche"
                created_at:
                  type: string
                  format: date-time
                  example: "2025-09-20 09:47:16"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-09-20 09:47:16"
          404:
            description: Post not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post not found"
        """
        return self.post_service.getPostById(post_id)
