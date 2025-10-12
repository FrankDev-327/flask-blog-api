from flask_restful import Resource, request
from middleware.check_token import require_token
from services.interesting_service import InterestingService

class ListingUserSameInterestController(Resource):
    def __init__(self):
        super().__init__()
        self.interesting_service = InterestingService()
        
    @require_token
    def get(self):
        
        user_id = request.user['id']
        interests = self.interesting_service.listingUsersSameInterest(user_id)        
        return { "user_id": user_id, "interests": interests }, 200