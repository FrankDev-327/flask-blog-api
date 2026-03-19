from flask_restful import Resource, request
from middleware.check_token import require_token
from services.comment_service import CommentService


class CommentController(Resource):
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()

    @require_token
    def post(self):
        """
        Create a new comment
        ---
        tags:
          - Comment
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                content:
                  type: string
                  example: "test_content_2000"
                post_id:
                  type: integer
                  example: 1
                user_id:
                  type: integer
                  example: 2
        responses:
          201:
            description: Comment successfully created
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Comment created
                comment:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 7
                    content:
                      type: string
                      example: test_content_2000
                    post_id:
                      type: integer
                      example: 1
                    user_id:
                      type: integer
                      example: 2
                    created_at:
                      type: string
                      format: date-time
                      example: "2025-09-21 00:51:46"
                    updated_at:
                      type: string
                      format: date-time
                      example: "2025-09-21 00:51:46"
        """
        comment_body = request.get_json(force=True)
        return self.comment_service.createComment(comment_body)
