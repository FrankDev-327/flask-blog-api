from flask_restful import Api
from controllers.interesting.creating_interesting_controller import (
    CreatingInterestingController,
)
from controllers.interesting.llisting_interesting_controller import (
    LListingInterestingController,
)
from controllers.interesting.listing_user_same_interest_controller import (
    ListingUserSameInterestController,
)


def register_interesting_route(api: Api):
    api.add_resource(
        LListingInterestingController,
        "/interesting",
        methods=["GET"],
        endpoint="interesting",
    )
    api.add_resource(
        CreatingInterestingController,
        "/interesting",
        methods=["POST"],
        endpoint="create_interesting",
    )
    api.add_resource(
        ListingUserSameInterestController,
        "/interesting/same-interest",
        methods=["GET"],
        endpoint="listing_user_same_interest",
    )
