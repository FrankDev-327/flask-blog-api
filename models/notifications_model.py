from connection import db 

class NotificationModel(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    type_notification = db.Column(db.String(10), nullable=True)
    notification_preview = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    