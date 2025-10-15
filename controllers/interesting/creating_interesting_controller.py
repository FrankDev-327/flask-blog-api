from flask_restful import Resource, request
from middleware.check_token import require_token
from services.interesting_service import InterestingService

class CreatingInterestingController(Resource):
    def __init__(self):
        super().__init__()
        self.interesting_service = InterestingService()
        
    @require_token
    def post(self):
        """
        Create Interesting Thing
        This endpoint allows an authenticated user to create a new interesting thing.

        ---
        tags:
          - Interesting
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                title:
                  type: string
                  example: "Interesting Title"
                description:
                  type: string
                  example: "This is a description of the interesting thing."
        responses:
          201:
            description: Interesting thing created successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Interesting thing created successfully"
                interesting_thing:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    title:
                      type: string
                      example: "Interesting Title"
                    description:
                      type: string
                      example: "This is a description of the interesting thing."
                    user_id:
                      type: integer
                      example: 1
                    created_at:
                      type: string
                      example: "2024-01-01 12:00:00"
                    updated_at:
                      type: string
                      example: "2024-01-01 12:00:00"
          400:
            description: Bad request (e.g., missing or invalid fields)
          401:
            description: Unauthorized
          500:
            description: Internal server error
        """
        
        user_id = request.user['id']
        interesting_body = request.get_json()
        return self.interesting_service.createInteresting(interesting_body, user_id)