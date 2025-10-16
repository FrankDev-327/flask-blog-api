from flask_restful import Resource, request
from middleware.check_token import require_token
from services.comment_service import CommentService


class CommentUpdateController(Resource):
    def __init__(self):
        super().__init__()
        self.comment_service = CommentService()

    @require_token
    def put(self, comment_id):
        """
        Update a comment
        ---
        tags:
          - Comment
        parameters:
          - name: comment_id
            in: path
            type: integer
            required: true
            description: ID of the comment to update
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                content:
                  type: string
                  example: "Updated comment content"
        responses:
          200:
            description: Comment updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Comment updated"
                comment:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 6
                    content:
                      type: string
                      example: "baño de semen en el ano de marisol sexo anal en el ano de marisol y despues de dejarle el ano super abierto llenarselo de bastante leche y maria se beba la leche desde el ano de marisol y despues se besen"
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
        comment_body = request.get_json(force=True)
        return self.comment_service.updateComment(comment_id, comment_body)
