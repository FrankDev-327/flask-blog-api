from serializabel_mixin import SerializableMixin
from connection import db  # Importing the db instance from connection.py

class UserModel(db.Model, SerializableMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    posts = db.relationship('PostModel', back_populates='user', lazy=True)
    comments = db.relationship('CommentModel', back_populates='user', lazy=True)
