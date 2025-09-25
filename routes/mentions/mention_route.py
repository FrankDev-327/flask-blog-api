from flask_restful import Api
from controllers.mentions.mention_list_user_controller import MentionListUserController


def register_mentions_routes(api: Api):
    api.add_resource(MentionListUserController, '/mentions', endpoint='mention_all')