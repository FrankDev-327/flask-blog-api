from flask_restful import Resource, request
from middleware.check_token import require_token
from services.mention_user_service import MentionService


class MentionListUserController(Resource):
    def __init__(self):
        super().__init__()
        self.mention_service = MentionService()

    @require_token
    def get(self):
        user_id = request.user["id"]
        return self.mention_service.list_comments_to_users(user_id)
