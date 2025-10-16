from flask_restful import Resource
from middleware.check_token import require_token
from services.comment_service import CommentService


class CommentGetDetailsController(Resource):
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()

    @require_token
    def get(self, comment_id):
        """
        Get details of a specific comment
        ---
        tags:
          - Comment
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
            description: ID of the comment
        responses:
          200:
            description: Comment details retrieved successfully
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 6
                content:
                  type: string
                  example: "baño de semen en el ano de marisol sexo anal en el ano de marisol y ..."
                post_id:
                  type: integer
                  example: 1
                user_id:
                  type: integer
                  example: 2
                created_at:
                  type: string
                  format: date-time
                  example: "2025-09-21 00:37:08"
                updated_at:
                  type: string
                  format: date-time
                  example: "2025-09-21 00:49:53"
          404:
            description: Comment not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Comment not found"
        """
        return self.comment_service.getCommentById(comment_id)
