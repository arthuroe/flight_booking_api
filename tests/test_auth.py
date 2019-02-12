import json
import unittest

from app.models import User
from tests import BaseTestCase


class TestAuth(BaseTestCase):

    def test_registration_successful(self):
        """
        Test for successful user registration
        """
        response = self.register_user('test', 'testing', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertEqual(response.status_code, 201)

    def test_registration_with_already_registered_username(self):
        """
        Test registration with an already registered username fails
        """
        user = User(username='test', password='test', name='test')
        user.save()
        response = self.register_user('test', 'test', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'User already exists. Please log in.')
        self.assertEqual(response.status_code, 409)

    def test_registration_with_incomplete_info(self):
        """
        Test for Incomplete input during registration
        """
        response = self.register_user('test', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Incomplete data. Username, name and '
                        'password must be provided')
        self.assertEqual(response.status_code, 400)

    def test_login_successful(self):
        """
        Test for successful user registration
        """
        response1 = self.register_user('test', 'testing', 'test')
        response = self.login_user('test', 'testing')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test that login of a non-registered user fails
        """
        response = self.login_user('test', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_with_missing_credentials(self):
        """
        Test that a user cannot login with missing credentials
        """
        response = self.login_user('test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] ==
                        'Username or password not provided.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)
