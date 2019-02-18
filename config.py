import os
from datetime import timedelta
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# # Create Celery beat schedule:
# celery_get_manifest_schedule = {
#     'schedule-name': {
#         'task': 'app.tasks.periodic_run',
#         'schedule': timedelta(seconds=50),
#     },
# }


class Config:
    """Parent configuration class."""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = os.environ.get('REDIS_URL') or 'redis://'
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL') or 'redis://'
    # CELERYBEAT_SCHEDULE = celery_get_manifest_schedule
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class DevelopmentConfiguration(Config):
    """Development configuration class."""
    DEBUG = True
    DEVELOPMENT = True


class TestingConfiguration(Config):
    """Testing configuration class."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flight_testing_db'


class ProductionConfiguration(Config):
    """Production configuration class."""
    DEBUG = False


app_configuration = {
    'production': ProductionConfiguration,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}
