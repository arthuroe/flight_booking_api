import re

from flask import request, jsonify, make_response
from functools import wraps

from app.models import User


def token_required(func):
    """
    Decorator function to ensure that a resource is access by only authenticated users
    provided their auth tokens are valid
    """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return make_response(jsonify({
                    'status': 'failed',
                    'message': 'Provide a valid auth token'
                })), 403

        if not token:
            return make_response(jsonify({
                'status': 'failed',
                'message': 'Token is missing'
            })), 401

        try:
            decode_response = User.decode_token(token)
            current_user = User.query.filter_by(id=decode_response).first()
        except:
            message = 'Invalid token'
            if isinstance(decode_response, str):
                message = decode_response
            return make_response(jsonify({
                'status': 'failed',
                'message': message
            })), 401
        return func(current_user, *args, **kwargs)

    return decorated_function


def validate_email(email):
    if re.search('[^@]+@[^@]+\.[^@]+', email):
        return True
    return False


def validate_password(password):
    LENGTH = re.compile(r'.{8,}')
    UPPERCASE = re.compile(r'[A-Z]')
    LOWERCASE = re.compile(r'[a-z]')
    DIGIT = re.compile(r'[0-9]')
    ALL_PATTERNS = (LENGTH, UPPERCASE, LOWERCASE, DIGIT)
    return all(pattern.search(password) for pattern in ALL_PATTERNS)
