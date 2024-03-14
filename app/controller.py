from flask import redirect, render_template, request
from flask_login import (
    AnonymousUserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import app, db, login_manager
from app.model import User


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@login_required
@app.route("/")
def main():
    return render_template("index.html")


@app.route("/menu")
def menu():
    if isinstance(current_user, AnonymousUserMixin):
        return "No"
    return render_template("form.html", name=current_user.name)


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

    return redirect("/menu")


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

    return redirect("/menu")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Ok"
