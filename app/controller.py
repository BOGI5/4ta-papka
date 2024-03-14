from flask import render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_mail import Message

from app import app, db, login_manager, mail
from app.model import *


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]

    exists = User.query.filter_by(email=email).first()
    if exists:
        return "Email is not available"

    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return "Ok"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()

    if not user:
        return "Invalid email"

    if user.password != password:
        return "Invalid password"

    login_user(user)

    return "Ok"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Ok"


def send_email(recipient, body: str):
    message = Message(subject="DishEat", recipients=[recipient])
    message.body = body
    mail.send(message)


def add_receipe(receipe_data: dict):
    receipe = Receipe(user=current_user["id"], label=receipe_data["Receipe"], total_time=receipe_data["Time to make"], 
                      calories=receipe_data["Calories"], ingridients=receipe_data["Ingredients"], instructions=receipe_data["Instructions"])
    db.session.add(receipe)
    db.session.commit()
