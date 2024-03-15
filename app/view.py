from flask import redirect, render_template, request
from flask_login import AnonymousUserMixin, current_user, login_required, login_user

from app import app, db
from app.ai_features import *
from app.controller import *
from app.model import Quiz, Recipe, User


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")


@app.route("/fridge", methods=["GET", "POST"])
def fridge():
    if request.method == "GET":
        return render_template("fridge.html")

    render_template("loading.html")
    image = request.form["imageData"].split("base64,")[1]
    recipe = generate_recipe_from_groceries_image(image)
    return render_template("recipe.html", recipe=recipe)


@app.route("/dish", methods=["GET", "POST"])
def dish():
    if request.method == "GET":
        return render_template("fridge.html")

    render_template("loading.html")
    image = request.form["imageData"].split("base64,")[1]
    recipe = generate_recipe_from_meal_image(image)
    return render_template("recipe.html", recipe=recipe)


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/")

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
            mode=request.form["goal"],
        )
        prev_quiz = Quiz.query.filter_by(user=current_user.id).first()
        if prev_quiz is not None:
            db.session.delete(prev_quiz)
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
        return render_template("signup.html", error=1)

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
        return render_template("login.html", error=1)

    if user.password != password:
        return render_template("login.html", error=2)

    login_user(user)

    return redirect("/calendar")


@app.route("/calendar")
def calendar():
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/")

    render_template("loading.html")
    days = get_recipes()
    return render_template("/calendar.html", days=days)


@app.route("/recipe/<int:recipe_id>")
def recipe_info(recipe_id):
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/")

    recipe = get_recipe_by_id(recipe_id)
    ingridients = recipe.ingridients.split(", ")
    return render_template("recipe.html", recipe=recipe, ingridients=ingridients)


@app.route("/order", methods=["GET", "POST"])
def get_user_info():
    if isinstance(current_user, AnonymousUserMixin):
        return redirect("/")

    if request.method == "GET":
        return render_template("order.html")

    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    phone = request.form["phone"]
    recipes = Recipe.query.filter_by(user=current_user.id).all()
    print(type(recipes))
    ingredients = " ".join([recipe.ingridients for recipe in recipes])

    email_prompt = generate_email(
        f"Address coordinates: {latitude}, {longitude} and phone number {phone}, email: {current_user.email}, sender name: {current_user.name}, ingredients: {ingredients}"
    )

    return send_email("kristiyan.p.simchev.2020@elsys-bg.org", email_prompt)
