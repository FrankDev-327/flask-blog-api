from connection import db 

class PrivateMessageModel(db.Model):
    __tablename__ = 'private_message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    sender = db.relationship('UserModel', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = db.relationship('UserModel', foreign_keys=[receiver_id], back_populates='received_messages')