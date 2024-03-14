from flask import redirect, render_template, request
from flask_login import (
    AnonymousUserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import app, db, login_manager
from app.model import User, Recipe


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@login_required
@app.route("/")
def main():
    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if isinstance(current_user, AnonymousUserMixin):
        return "No"
    if request.method == "GET":
        return render_template("form.html", name=current_user.name)

    return {
        "time": request.form["time"],
        "allergic": request.form["allergic"],
        "meals_count": request.form["meals_count"],
        "preference": request.form["preference"],
        "appliances": request.form["appliances"],
        "skill_level": request.form["skill_level"],
    }


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

    return redirect("/quiz")


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



def save_recipe(recipe_info: dict):
    recipe = Recipe(user=current_user.id, label=recipe_info["Recipe"], total_time=recipe_info["Time to make"],
                    calories=recipe_info["Calories"], ingridients=recipe_info["Ingredients"], instructions=recipe_info["Instructions"])
    try:
        db.session.add(recipe)
        db.session.commit()
    except Exception:
        return "This meal exists!"

