import os
from flask import Flask
from config import app_configuration
# from app.models.model_mixin import db


app = Flask(__name__)

# db.init_app(app)
# app configuration
environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])

# db.app = app
# db.init_app(app)
