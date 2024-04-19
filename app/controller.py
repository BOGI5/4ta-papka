from datetime import datetime, timedelta

from flask import redirect
from flask_login import AnonymousUserMixin, current_user, login_required, logout_user
from flask_mail import Message

from app import app, db, login_manager, mail
from app.ai_features import calculate_calendar
from app.model import Quiz, Recipe, User, UnautorizedUser


@login_manager.user_loader
def user_loader(id):
    if UnautorizedUser.query.get(id):
        return UnautorizedUser.query.get(id)
    else:
        return User.query.get(id)


@app.route("/delete_user")
@login_required
def delete_user():
    if isinstance(current_user, AnonymousUserMixin) or isinstance(current_user, UnautorizedUser):
        return redirect("/")

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
    if isinstance(current_user, AnonymousUserMixin) or isinstance(current_user, UnautorizedUser):
        return redirect("/")

    logout_user()
    return redirect("/")


def get_recipes():
    temp = Recipe.query.filter_by(user=current_user.id).all()
    temp = sorted(temp, key=lambda x: (x.date, x.meal_order))
    days = []
    for i in range(0, 7):
        days.append([])
    for i in range(0, len(temp)):
        day = (temp[i].date - datetime.now().date()).days
        if day >= 0:
            days[day].append(temp[i])
    return days


def get_recipe_by_id(id: int):
    return Recipe.query.get(id)


def generate_calendar():
    quiz = get_user_quiz()
    quiz_dict = {
        "time": quiz.time,
        "allergic": quiz.allergic,
        "meals_per_day": quiz.meals_count,
        "preference": quiz.preference,
        "appliances": quiz.appliances,
        "skill_level": quiz.skill_level,
        "mode": quiz.mode,
    }
    calendar = calculate_calendar(quiz_dict)
    for i in range(0, 7):
        recipes_list = calendar[f"Day {1 + i}"]
        for j in range(0, len(recipes_list)):
            save_recipe(recipes_list[j], (datetime.now() + timedelta(days=i)), j + 1)


def save_recipe(recipe_info: dict, date: datetime, meal_order: int):
    recipe = Recipe(
        user=current_user.id,
        label=recipe_info["label"],
        total_time=recipe_info["totalTime"],
        calories=recipe_info["calories"],
        ingridients=recipe_info["ingredients"],
        instructions=recipe_info["instructions"],
        number_of_meals=recipe_info["number_of_meals"],
        date=date,
        meal_order=meal_order,
    )
    try:
        db.session.add(recipe)
        db.session.commit()
    except Exception:
        return "This meal exists!"


def get_user_quiz():
    return Quiz.query.filter_by(user=current_user.id).first()


def send_email(subject: str, recipient: str, body: str):
    message = Message(subject=subject, recipients=[recipient])
    message.body = body
    mail.send(message)
    return redirect("/")
