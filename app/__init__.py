from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
USERNAME, PASSWORD, HOST, DATABASE_NAME = "MyUser", "MyPassword", "localhost", "Users"
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE_NAME}"
)
app.config["SECRET_KEY"] = "MySecretKey"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
