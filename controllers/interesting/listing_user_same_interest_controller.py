from flask_restful import Resource, request
from middleware.check_token import require_token
from services.interesting_service import InterestingService

class ListingUserSameInterestController(Resource):
    def __init__(self):
        super().__init__()
        self.interesting_service = InterestingService()
        
    @require_token
    def get(self):
        """
        Get users with the same interests
        ---
        tags:
          - Interests
        summary: Get users who share the same interests as the authenticated user
        description: |
          This endpoint returns a list of users who share the same interests as the authenticated user.
          The request must include a valid Bearer token for authentication.
        security:
          - BearerAuth: []
        responses:
          200:
            description: Successfully retrieved users with similar interests
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    user_id:
                      type: integer
                      example: 3
                      description: ID of the authenticated user
                    interests:
                      type: array
                      description: List of users sharing the same interests
                      items:
                        type: object
                        properties:
                          user_id:
                            type: integer
                            example: 13
                          nick_name:
                            type: string
                            example: test_nich_name_user_31
          401:
            description: Unauthorized - invalid or missing token
          500:
            description: Internal server error
        """
        
        user_id = request.user['id']
        interests = self.interesting_service.listingUsersSameInterest(user_id)        
        return { "user_id": user_id, "interests": interests }, 200
