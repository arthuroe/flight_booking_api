import os

from flask import Flask
from flask_mail import Mail

from config import app_configuration


app = Flask(__name__)
mail = Mail(app)


environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])


from app.models import db
from app.auth import auth_blueprint
from app.flights import flight_blueprint
from app.booking import booking_blueprint

db.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(flight_blueprint)
app.register_blueprint(booking_blueprint)
