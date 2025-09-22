from connection import db 

class MentionModel(db.Model):
    __tablename__ = "mentiones"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comments.id"))
    mentioned_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    