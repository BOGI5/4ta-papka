from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    TEXT_MAX_SIZE = 300
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(TEXT_MAX_SIZE), nullable=False, unique=True)
    name = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    password = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)

    def __repr__(self) -> str:
        return f"Email: {self.email}"
