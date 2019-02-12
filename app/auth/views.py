import logging

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.models import User


class RegisterView(MethodView):
    """
    View to register a user
    """

    def post(self):
        post_data = request.json

        username = post_data.get('username')
        name = post_data.get('name')
        password = post_data.get('password')

        if not all([username, name, password]):
            response = {
                'status': 'fail',
                'message': ('Incomplete data. Username, name and '
                            'password must be provided')
            }
            return make_response(jsonify(response)), 400

        user = User.find_first(username=post_data.get('username'))
        if not user:
            try:
                user = User(username=username, password=password, name=name)
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
