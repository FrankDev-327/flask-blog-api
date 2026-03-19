from flask_restful import Resource, request
from services.post_service import PostService
from middleware.check_token import require_token


class PostGetSearchTitleController(Resource):
    def __init__(self):
        super().__init__()
        self.post_service = PostService()

    @require_token
    def get(self):
        """
        Search posts by title
        ---
        tags:
          - Post
        parameters:
          - name: title
            in: query
            type: string
            required: true
            description: Title (or partial) to search posts
            example: marisol_zorra_bebedora_de_semen_por_el_ano
        responses:
          200:
            description: Posts found matching the title
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Posts found
                post:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 31
                      title:
                        type: string
                        example: marisol_zorra_bebedora_de_semen_por_el_ano
                      content:
                        type: string
                        example: bebedora de semen no dejaba nada de leche de mi verga.. toda tragada perra zorra puta golfa...
                      created_at:
                        type: string
                        example: 2025-09-22 09:14:48
                      updated_at:
                        type: string
                        example: 2025-09-22 09:14:48
        """
        title = request.args.get("title", "", type=str)
        return self.post_service.get_post_by_title(title)
