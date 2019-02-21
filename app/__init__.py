from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

from app import routes, models
from app.dash import dash
from app.farer import farer

app.register_blueprint(dash, url_prefix='/dash')
app.register_blueprint(farer, url_prefix='/farer')
