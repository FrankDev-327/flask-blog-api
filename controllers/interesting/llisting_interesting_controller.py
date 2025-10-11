from flask_restful import Resource
from constants import list_interesting
from middleware.check_token import require_token

class LListingInterestingController(Resource):
    def __init__(self):
        super().__init__()
        
    @require_token
    def get(self):
        return { "interesting": list_interesting }, 200