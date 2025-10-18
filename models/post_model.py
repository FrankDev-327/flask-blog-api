from connection import db


class PostModel(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    images = db.relationship("ImagesModel", back_populates="post", lazy=True)
    comments = db.relationship("CommentModel", back_populates="post", lazy=True)
    user = db.relationship("UserModel", back_populates="posts", lazy=True)
