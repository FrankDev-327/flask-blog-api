from flask import Flask
from serializabel_mixin import SerializableMixin
from connection import db  # Importing the db instance from connection.py

class PostModel(db.Model, SerializableMixin):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    user = db.relationship('UserModel', back_populates='posts', lazy=True)  # ✅ corrected
    comments = db.relationship('CommentModel', back_populates='post', lazy=True)