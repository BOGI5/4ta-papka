from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

USERNAME, PASSWORD, HOST, DATABASE_NAME = "MyUser", "MyPassword", "localhost", "Users"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
)
app.config["SECRET_KEY"] = "MySecretKey"

db = SQLAlchemy(app)


class User(db.Model):
    TEXT_MAX_SIZE = 300
    email = db.Column(db.String(TEXT_MAX_SIZE), primary_key=True)
    name = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)
    password = db.Column(db.String(TEXT_MAX_SIZE), nullable=False)

    def __repr__(self) -> str:
        return f"Email: {self.email}"


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

    exists = db.session.query(User).filter_by(email=email).first()
    if exists:
        return "Email is not available"

    user = User(email=email, name=name, password=password)
    db.session.add(user)
    db.session.commit()

    return name


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    password = request.form["password"]


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)
