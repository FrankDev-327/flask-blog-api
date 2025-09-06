from serializabel_mixin import SerializableMixin
from connection import db 

class TokenModel(db.Model, SerializableMixin):
    __tablename__ = 'tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text, nullable=False, unique=True)
    marked_as_used = db.Column(db.Boolean, default=False)