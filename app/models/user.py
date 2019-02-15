import jwt
import logging

from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

from .model_mixin import db, ModelMixin
from app import app


class User(ModelMixin):
    """
    User model attributes
    """
    __tablename__ = 'users'

    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    bookings = db.relationship('Booking', backref='users', lazy='dynamic')

    def __init__(self, username, password, name):
        """
        Initializes the user instance
        """
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.name = name

    def password_is_valid(self, password):
        """
        Check the password against its hash to validate it
        """
        return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def generate_token(user_id):
        """
        Generate access token
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(hours=4),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            logging.error(f"An error while generating a token {e}")
            return str(e)

    @staticmethod
    def decode_token(token):
        """
        Decodes the access token from the Authorization header.
        """
        try:
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"
