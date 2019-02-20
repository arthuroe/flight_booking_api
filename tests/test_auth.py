import json
import unittest
import os

from app.models import User
from tests import BaseTestCase


class TestAuth(BaseTestCase):

    def test_registration_successful(self):
        """
        Test for successful user registration
        """
        response = self.register_user('test@gmail.com', 'tesTing123', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertEqual(response.status_code, 201)

    def test_registration_with_already_registered_username(self):
        """
        Test registration with an already registered username fails
        """
        user = User(username='test@gmail.com',
                    password='tesTing123', name='test')
        user.save()
        response = self.register_user('test@gmail.com', 'tesTing123', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'User already exists. Please log in.')
        self.assertEqual(response.status_code, 409)

    def test_registration_with_incomplete_info(self):
        """
        Test for Incomplete input during registration
        """
        response = self.register_user('testing@gmail.com', 'testIng123')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(
            data['message'] == 'Incomplete data. Username, name and '
            'password must be provided'
        )
        self.assertEqual(response.status_code, 400)

    def test_login_successful(self):
        """
        Test for successful user registration
        """
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response = self.login_user('test@gmail.com', 'tesTing123')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """
        Test that login of a non-registered user fails
        """
        response = self.login_user('test@gmail.com', 'tesTing123')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'User does not exist.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_with_missing_credentials(self):
        """
        Test that a user cannot login with missing credentials
        """
        response = self.login_user('test@gmail.com')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] ==
                        'Username or password not provided.')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_validations_on_login(self):
        """
        Test validations on user input when logging in.
        """
        response = self.login_user('test', '12344')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] ==
                        'Invalid Username or password provided')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_validations_on_register(self):
        """
        Test validations on user input when registering.
        """
        response = self.register_user('test@gmail.com', 'tes123', 'test')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] ==
                        'Invalid Email or password provided')
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_upload_image(self):
        """
        Test successfull image upload
        """
        register = self.register_user('test@gmail.com', 'tesTing123', 'test')
        login = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(login.data.decode())['auth_token']
        asset = "test.jpg"
        path = os.path.join(f"./tests/assets/{asset}")
        response = self.client.post(
            '/api/v1/image_upload',
            headers=dict(Authorization="Bearer " + access_token),
            data={'item': open(path, 'rb')},
            content_type='multipart/form-data'
        )
        self.assertEqual(response.status_code, 201)
