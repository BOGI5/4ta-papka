from flask import Flask, render_template, request
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

USERNAME, PASSWORD, HOST, DATABASE_NAME = "disheat", "MyPassword", "localhost", "Users"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
)
app.config["SECRET_KEY"] = "MySecretKey"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    TEXT_MAX_SIZE = 300
    email = db.Column(db.String(TEXT_MAX_SIZE), primary_key=True)
    name = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    password = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)

    def get_id(self):
        return self.email

    def __repr__(self) -> str:
        return f"Email: {self.email}"


@login_manager.user_loader
def user_loader(email):
    return User.query.get(email)


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

    if user_loader(email):
        return "Email is not available"

    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return current_user


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]

    user = user_loader(email)
    if not user:
        return "Invalid email"

    if user.password != password:
        return "Invalid password"

    login_user(user)


@app.route("/logout")
@login_required
def logout():
    logout_user()


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)
