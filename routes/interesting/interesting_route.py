from flask_restful import Api
from controllers.interesting.llisting_interesting_controller import LListingInterestingController

def register_interesting_route(api: Api):
    api.add_resource(LListingInterestingController, '/interesting', methods=['GET'], endpoint='interesting')
