from flask_restful import Resource, request
from middleware.check_token import require_token
from services.post_service import PostService


class PostUpdateController(Resource):
    def __init__(self):
        super().__init__()
        self.post_service = PostService()

    @require_token
    def put(self, post_id):
        """
        Update an existing post
        ---
        tags:
          - Post
        parameters:
          - name: post_id
            in: path
            type: integer
            required: true
            description: ID of the post to update
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - title
                - content
              properties:
                title:
                  type: string
                  example: "test_post_100000000"
                content:
                  type: string
                  example: "bebedora de semen no dejaba nada de leche de mi verga.. toda tragada perra zorra puta golfa jerioth se bebia mi semen por el ano y a veces se lo echaba en la cara o se lo tragaba toda la leche"
        responses:
          200:
            description: Post updated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post created"
                post:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    title:
                      type: string
                      example: "test_post_100000000"
                    content:
                      type: string
                      example: "bebedora de semen no dejaba nada de leche de mi verga.. toda tragada perra zorra puta golfa jerioth se bebia mi semen por el ano y a veces se lo echaba en la cara o se lo tragaba toda la leche"
                    user_id:
                      type: integer
                      example: 1
                    created_at:
                      type: string
                      format: date-time
                      example: "2025-08-30 20:12:26"
                    updated_at:
                      type: string
                      format: date-time
                      example: "2025-09-21 13:29:41"
          400:
            description: Invalid input
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Invalid request body"
          404:
            description: Post not found
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Post not found"
        """
        post_body = request.get_json(force=True)
        return self.post_service.updatePost(post_id, post_body)
