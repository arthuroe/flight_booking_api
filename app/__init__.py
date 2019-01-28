import os
from flask import Flask
from config import app_configuration


app = Flask(__name__)

# app configuration
environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])
