import os
import cloudinary

from celery import Celery
from flask import Flask
from flask_mail import Mail

from config import app_configuration
import celery_config

app = Flask(__name__)


environment = os.getenv("APP_SETTINGS")
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app.config.from_object(app_configuration[environment])
mail = Mail(app)


from app.models import db
from app.auth import auth_blueprint
from app.flights import flight_blueprint
from app.booking import booking_blueprint

db.init_app(app)

from app import error_handlers

app.register_blueprint(auth_blueprint)
app.register_blueprint(flight_blueprint)
app.register_blueprint(booking_blueprint)


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    celery.config_from_object(celery_config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context().push():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('CLOUD_API_KEY'),
    api_secret=os.environ.get('CLOUD_API_SECRET')
)


@app.route('/')
def index():
    return "Welcome to the Flight Booking Api"
