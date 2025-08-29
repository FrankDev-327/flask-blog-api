from serializabel_mixin import SerializableMixin
from connection import db  # Importing the db instance from connection.py

class CommentModel(db.Model, SerializableMixin):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    limit_comment = db.Column(db.Boolean, default=True)

    post = db.relationship('PostModel', back_populates='comments')
    user = db.relationship('UserModel', back_populates='comments')