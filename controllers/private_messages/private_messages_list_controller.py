from middleware.check_token import require_token
from services.private_message_service import PrivateMessageService
from flask_restful import Resource, request

class PrivateMessagesListController(Resource):  
    def __init__(self):
        super().__init__()
        self.private_message_service = PrivateMessageService()
        
    @require_token
    def get(self):
        """
        Get private messages between sender and receiver
        ---
        tags:
          - Private Messages
        parameters:
          - name: sender_id
            in: query
            required: true
            type: integer
            example: 1
          - name: receiver_id
            in: query
            required: true
            type: integer
            example: 2
        responses:
          200:
            description: List of private messages retrieved successfully
            schema:
              type: object
              properties:
                private_message:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      content:
                        type: string
                        example: "Hello, how are you?"
                      sender_id:
                        type: integer
                        example: 1
                      receiver_id:
                        type: integer
                        example: 2
                      created_at:
                        type: string
                        example: "2023-10-01 12:00:00"
                      updated_at:
                        type: string
                        example: "2023-10-01 12:00:00"
          500:
            description: Error retrieving private messages
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error retrieving private messages"
        """
        sender_id = request.args.get('sender_id', type=int)
        receiver_id = request.args.get('receiver_id', type=int)
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        
        if not sender_id or not receiver_id:
            return {'message': 'sender_id and receiver_id are required and must be integers'}, 400
        
        return self.private_message_service.get_private_message_by_id(sender_id, receiver_id, page, per_page)