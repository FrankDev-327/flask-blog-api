from flask_restful import Resource, request
from middleware.check_token import require_token
from services.notifications_service import NotificationService

class NotificationController(Resource):
    def __init__(self):
        super().__init__()
        self.notification_service = NotificationService()
        
    @require_token
    def get(self):
        """
        List Notifications
        This endpoint retrieves notifications for the authenticated user.

        ---
        tags:
          - Notifications
        security:
          - Bearer: []
        responses:
          200:
            description: List of notifications
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "List of notifications"
                notifications:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      comment_id:
                        type: integer
                        example: 130
                      type_notification:
                        type: string
                        example: "notification"
                      notification_preview:
                        type: string
                        example: "test_user_20 test extract use"
          401:
            description: Unauthorized
          500:
            description: Internal server error
        """
        user_id = request.user['id']
        return self.notification_service.list_user_notifications(user_id)
