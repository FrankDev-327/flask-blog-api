from flask_restful import Resource, request
from middleware.check_token import require_token
from services.contact_service import ContactService 

class CreateNewContactController(Resource): 
    def __init__(self):
        super().__init__()
        self.contact_service = ContactService()
        
    @require_token
    def post(self):
        """
        Create New Contact
        This endpoint allows an authenticated user to create a new contact.

        ---
        tags:
          - Contacts
        security:
          - Bearer: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                contact_id:
                  type: integer
                  example: 2
        responses:
          201:
            description: Contact request sent successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Contact request sent"
                contact:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    user_id:
                      type: integer
                      example: 1
                    contact_id:
                      type: integer
                      example: 2
                    status:
                      type: string
                      example: "pending"
                    created_at:
                      type: string
                      example: "2024-01-01 12:00:00"
          400:
            description: Bad Request (e.g., missing parameters, contact already exists)
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: user_id and contact_id are required" or Contact already exists
          500:
            description: Internal Server Error
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Error adding contact: <error details>"
        """
        data = request.get_json()
        contact_id = data.get('contact_id')
        user_id = request.user['id']
        
        return self.contact_service.add_contact(user_id, contact_id)    