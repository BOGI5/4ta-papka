from datetime import datetime

from flask import redirect, render_template, request
from flask_login import (
    AnonymousUserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import app, db, login_manager
from app.generate_calendar import calculate_calendar
from app.get_groceries_from_image import get_groceries_from_image
from app.model import Quiz, Recipe, User


@login_manager.user_loader
def user_loader(id):
    return User.query.get(id)


@login_required
@app.route("/")
def main():
    return render_template("index.html")


@app.route("/fridge", methods=["GET", "POST"])
def get_image():
    if request.method == "GET":
        return render_template("fridge.html")

    image = request.form["imageData"].split("base64,")[1]

    return get_groceries_from_image(image)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if isinstance(current_user, AnonymousUserMixin):
        return "No"
    if request.method == "GET":
        return render_template("form.html", name=current_user.name)

    elif request.method == "POST":
        quiz = Quiz(
            user=current_user.id,
            time=request.form["time"],
            allergic=request.form["allergic"],
            meals_count=request.form["meals_count"],
            preference=request.form["preference"],
            appliances=request.form["appliances"],
            skill_level=request.form["skill_level"],
        )
        if Quiz.query.exists(user=current_user.id):
            db.session.delete(Quiz.query.filter_by(user=current_user.id))
            prev_recipes = Recipe.query.filter_by(user=current_user.id).all()
            for recipe in prev_recipes:
                db.session.delete(recipe)
            db.session.commit()
        try:
            db.session.add(quiz)
            db.session.commit()
        except Exception:
            return "Error"
        generate_calendar()
        return redirect("/calendar")


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

    return redirect("/calendar")


@app.route("/delete_user")
@login_required
def delete_user():
    db.session.delete(Quiz.query.filter_by(user=current_user.id).first())
    recipes = Recipe.query.filter_by(user=current_user.id).all()
    for recipe in recipes:
        db.session.delete(recipe)
    temp = current_user
    logout_user()
    db.session.delete(temp)
    db.session.commit()
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


def get_recipes():
    temp = Recipe.query.filter_by(user=current_user.id).all()
    temp = sorted(temp, key=lambda x: x.day)
    days = []
    for i in range(0, 7):
        days.append([])
    for i in range(0, len(temp)):
        days[int(temp[i].day) - 1].append(temp[i])
    return days


def get_recipe_by_id(id: int):
    return Recipe.query.get(id)


@app.route("/calendar")
def calendar():
    days = get_recipes()
    return render_template("/calendar.html", days=days)


def generate_calendar():
    quiz = get_user_quiz()
    quiz_dict = {
        "time": quiz.time,
        "allergic": quiz.allergic,
        "meals_per_day": quiz.meals_count,
        "preference": quiz.preference,
        "appliances": quiz.appliances,
        "skill_level": quiz.skill_level,
    }
    calendar = calculate_calendar(quiz_dict)
    for i in range(0, 7):
        recipes_list = calendar[f"Day {1 + i}"]
        for j in range(0, len(recipes_list)):
            save_recipe(recipes_list[j], (1 + i) + ((j + 1) / 10))


@app.route("/recipe/<int:recipe_id>")
def recipe_info(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    ingridients = recipe.ingridients.split(", ")
    return render_template("recipe.html", recipe=recipe, ingridients=ingridients)


def save_recipe(recipe_info: dict, day: float):
    recipe = Recipe(
        user=current_user.id,
        label=recipe_info["label"],
        total_time=recipe_info["totalTime"],
        calories=recipe_info["calories"],
        ingridients=recipe_info["ingredients"],
        instructions=recipe_info["instructions"],
        number_of_meals=recipe_info["number_of_meals"],
        day=day,
    )
    try:
        db.session.add(recipe)
        db.session.commit()
    except Exception:
        return "This meal exists!"


def get_user_quiz():
    return Quiz.query.filter_by(user=current_user.id).first()
