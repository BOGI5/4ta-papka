from app import db

class User(db.Model):
    TEXT_MAX_SIZE = 300
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    name = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    password = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)

    def __repr__(self) -> str:
        return f"Email: {self.email}"
    
    __table_args__ = (
        db.UniqueConstraint('email'),
    )
