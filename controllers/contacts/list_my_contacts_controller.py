from flask_restful import Resource, request
from middleware.check_token import require_token
from services.contact_service import ContactService


class ListMyContactsControler(Resource):
    def __init__(self):
        super().__init__()
        self.contact_service = ContactService()

    @require_token
    def get(self):
        """
        List all my contacts
        ---
        tags:
          - Contacts
        summary: Get the authenticated user's contact list
        description: Returns all contacts associated with the authenticated user. A valid Bearer token is required.
        security:
          - BearerAuth: []
        responses:
          200:
            description: Successfully retrieved the contact list
            schema:
              type: object
              properties:
                contacts:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 9
                      user_id:
                        type: integer
                        example: 3
                      contact_id:
                        type: integer
                        example: 18
                      status:
                        type: string
                        example: pending
                      created_at:
                        type: string
                        example: "2025-10-15 06:56:50"
          401:
            description: Unauthorized - missing or invalid token
          500:
            description: Internal server error
        """
        user_id = request.user["id"]
        return self.contact_service.get_contacts(user_id)
