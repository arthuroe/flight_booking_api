import logging
import os

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from werkzeug.utils import secure_filename

from app import cloudinary
from app.auth.helpers import *
from app.models import User


class RegisterView(MethodView):
    """
    View to register a user
    """

    def post(self):
        kwargs = request.json
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not all([email, password, kwargs.get('name')]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. email, name and '
                            'password must be provided')
            }
            return make_response(jsonify(response)), 400

        if not validate_email(email) or not validate_password(password):
            response = {
                'status': 'fail',
                'message': ('Invalid Email or password provided'),
                'required': (
                    'Passwords should be at least 8 characters, contain'
                    ' a digit, uppercase and lowercase characters'
                )
            }
            return make_response(jsonify(response)), 400

        user = User.find_first(email=email)
        if not user:
            try:
                user = User(**kwargs)
                user.save()

                auth_token = user.generate_token(user.id)
                response = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                logging.error(f"An error has occurred  {e}")
                response = {
                    'status': 'fail',
                    'message': 'Registration failed. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please log in.',
            }
            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    """
    View to login the user
    """

    def post(self):
        post_data = request.json
        email = post_data.get('email')
        password = post_data.get('password')

        if not email or not password:
            response = {
                'status': 'fail',
                'message': 'email or password not provided.'
            }
            return make_response(jsonify(response)), 400

        if not validate_email(email):
            response = {
                'status': 'fail',
                'message': 'Invalid email or password provided'
            }
            return make_response(jsonify(response)), 400

        try:
            user = User.find_first(email=email)
            if user and user.password_is_valid(password):
                auth_token = user.generate_token(user.id)
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            logging.error(f"An error has occurred  {e}")
            response = {
                'status': 'fail',
                'message': 'An error has occurred. Please try again.'
            }
            return make_response(jsonify(response)), 500


class ImageUploadView(MethodView):
    """
    View for uploading passport_photo
    """
    decorators = [token_required]

    def post(self, current_user):
        file_item = request.files['item']
        if file_item:
            upload_result = upload(file_item)
            image_url = upload_result.get('url')
            user_id = current_user.id
            user = User.find_first(id=user_id)
            user.passport_photo = image_url
            user.save()
            response = {
                'status': 'success',
                'message': 'Image uploaded successfully.'
            }
            return make_response(jsonify(response)), 201

        else:
            response = {
                'status': 'fail',
                'message': 'Provide a file.'
            }
            return make_response(jsonify(response)), 400
