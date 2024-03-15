from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
