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
from app.model import Quiz, Recipe, User

from datetime import datetime


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
        try:
            db.session.add(quiz)
            db.session.commit()
        except Exception:
            return "Error"
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

    return redirect("/menu")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Ok"


def get_recipes():
    temp = Recipe.query.filter_by(user=current_user.id).all().order_by(Recipe.day)
    days = []
    for i in range(0, 7):
        days.append([])
    for i in range(0, len(temp)):
        days[temp[i].day / 1].append(temp[i])
    return days



@app.route("/calendar")
def calendar():
    quiz = get_user_quiz()
    quiz_dict = {
            "time": quiz.time,
            "allergic": quiz.allergic,
            "meals_per_day": quiz.meals_count,
            "preference": quiz.preferences,
            "appliances": quiz.appliances,
            "skill_level": quiz.skill_level,
        }
    calendar = calculate_calendar(quiz_dict)
    for i in range(0, 7):
        recipes_list = calendar[f"Day {1 + i}"]
        for j in range(0, len(recipes_list)):
            save_recipe(recipes_list[j], (1 + i) + ((j + 1) / 10))
    days = get_recipes()
    # ingridients = []
    # for i in range(0, len(recipes)):
    #    ingridients.append(recipes[i].split(""))
    return render_template("/calendar.html", days=days)

  
def save_recipe(recipe_info: dict, day: float):
    recipe = Recipe(
        user=current_user.id,
        label=recipe_info["Recipe"],
        total_time=recipe_info["Time to make"],
        calories=recipe_info["Calories"],
        ingridients=recipe_info["Ingredients"],
        instructions=recipe_info["Instructions"],
        number_of_meals=recipe_info["number_of_meals"],
        day=day
    )
    try:
        db.session.add(recipe)
        db.session.commit()
    except Exception:
        return "This meal exists!"
    

def get_user_quiz():
    return Quiz.query.filter_by(user=current_user.id).first
