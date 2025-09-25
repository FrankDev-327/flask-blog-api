from connection import db 
from datetime import datetime, timezone

class NotificationModel(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer(), nullable=False)
    notification_preview = db.Column(db.Text, nullable=False)
    type_notification = db.Column(db.String(10), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    user_mentioned_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    