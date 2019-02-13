import os

from flask import Flask

from config import app_configuration


app = Flask(__name__)


environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])


from app.models import db
from app.auth import auth_blueprint
from app.flights import flight_blueprint

db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(flight_blueprint)
