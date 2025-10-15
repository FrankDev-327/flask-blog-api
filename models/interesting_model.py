from connection import db 

class InterestingModel(db.Model):
    __tablename__ = 'interesting'
    id = db.Column(db.Integer, primary_key=True)
    interest_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    
    user = db.relationship(
        'UserModel',
        foreign_keys=[user_id], # This is correct (or can often be omitted)
        back_populates='interesting_user'
    )
    