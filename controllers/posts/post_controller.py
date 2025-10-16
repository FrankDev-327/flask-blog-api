from middleware.check_token import require_token
from services.post_service import PostService
from flask_restful import Resource, request


class PostCreateController(Resource):
    def __init__(self):
        super().__init__()
        self.post_service = PostService()

    @require_token
    def post(self):
        """
        Create a new post
        ---
        tags:
          - Post
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - title
                - content
                - user_id
              properties:
                title:
                  type: string
                  example: "test_post_1000"
                content:
                  type: string
                  example: "bebedora de semen no dejaba nada de leche de mi verga.. toda tragada perra zorra puta golfa jerioth se bebia mi semen por el ano y a veces se lo echaba en la cara o se lo tragaba toda la leche"
                user_id:
                  type: integer
                  example: 1
        responses:
          201:
            description: Post created successfully
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
                      example: 28
                    title:
                      type: string
                      example: "test_post_1000"
                    content:
                      type: string
                      example: "bebedora de semen no dejaba nada de leche de mi verga.. toda tragada perra zorra puta golfa jerioth se bebia mi semen por el ano y a veces se lo echaba en la cara o se lo tragaba toda la leche"
                    user_id:
                      type: integer
                      example: 1
                    created_at:
                      type: string
                      format: date-time
                      example: "2025-09-20 22:19:49"
                    updated_at:
                      type: string
                      format: date-time
                      example: "2025-09-20 22:19:49"
          400:
            description: Invalid input
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Invalid request body"
        """
        post_body = request.get_json(force=True)
        return self.post_service.createPost(post_body)
