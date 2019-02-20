import json

from datetime import datetime

from app.models import User
from tests import BaseTestCase


class TestFlight(BaseTestCase):

    def test_viewing_available_flights(self):
        """
        Test to see available flights
        """
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']
        response = self.client.get(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'success')
        self.assertEqual(response.status_code, 200)

    def test_adding_flights(self):
        """
        Test adding flight
        """
        user = User(username='test@gmail.com',
                    password='tesTing123', name='test', role=True)
        user.save()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']
        response = self.client.post(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(
                name='Kenya Airways', destination='London', number='KQ-17',
                capacity=2, date="2019-03-12 06:30:00"
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'success')
        self.assertEqual(response.status_code, 201)

    def test_viewing_flights_after_being_added(self):
        """
        Test viewing flights with flights available
        """
        user = User(username='test@gmail.com',
                    password='tesTing123', name='test', role=True)
        user.save()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']
        add_flight = self.client.post(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(
                name='Kenya Airways', destination='London', number='KQ-17',
                capacity=2, date="2019-03-12 06:30:00"
            )),
            content_type='application/json'
        )
        response = self.client.get(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'success')
        self.assertEqual(response.status_code, 200)

    def test_adding_flights_without_required_fields(self):
        """
        Test adding flight without required fields
        """
        user = User(username='test@gmail.com',
                    password='tesTing123', name='test', role=True)
        user.save()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']
        response = self.client.post(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(
                name='Kenya Airways', destination='London', number='KQ-17',
                capacity=2
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)

    def test_adding_flights_without_authorization(self):
        """
        Test adding flight without required fields
        """
        user = User(username='test@gmail.com',
                    password='tesTing123', name='test')
        user.save()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']
        response = self.client.post(
            '/api/v1/flights',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(
                name='Kenya Airways', destination='London', number='KQ-17',
                capacity=2
            )),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 401)
