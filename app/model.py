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
    

class Recipe(db.Model):
    TEXT_MAX_SIZE = 300
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    label = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    total_time = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    ingridients = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    instructions = db.Column(db.String(5000), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('label', 'user'),
    )


class Quiz(db.Model):
    TEXT_MAX_SIZE = 300
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    time = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    allergic = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    meals_count = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    preference = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    appliances = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    skill_level = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
