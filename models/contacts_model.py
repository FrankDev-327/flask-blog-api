from connection import db


class ContactsModel(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(
        db.Enum("pending", "accepted", "blocked", name="statusfriendenum"),
        default="pending",
        nullable=False,
    )
    created_at = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship(
        "UserModel", foreign_keys=[user_id], back_populates="contacts"
    )
    contact = db.relationship("UserModel", foreign_keys=[contact_id])
