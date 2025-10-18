from connection import db


class ImagesModel(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    ext_file = db.Column(db.String(4), nullable=True)
    url_file = db.Column(db.String(), nullable=False)
    size_file = db.Column(db.Integer(), nullable=True)
    public_id = db.Column(db.String(), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    post = db.relationship(
        "PostModel",
        foreign_keys=[post_id],  # This is correct (or can often be omitted)
        back_populates="images",
    )
