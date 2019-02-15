import json

from datetime import datetime

from app.models import Flight
from tests import BaseTestCase


class TestBooking(BaseTestCase):

    def test_booking_flight_successfully(self):
        """
        Test booking a flight Successfully
        """
        flight = Flight(
            flight_name='Kenya Airways', flight_number='KQ-123',
            flight_date=datetime(2019, 3, 3, 10, 10, 10),
            flight_destination='Kampala', capacity=45)
        flight.save()
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response = self.client.post(
            '/api/v1/booking', headers=dict(Authorization="Bearer " + access_token), data=json.dumps(
                dict(flight_id=1)), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'success')
        self.assertEqual(response.status_code, 201)

    def test_booking_flight_unsuccessfully(self):
        """
        Test booking a flight unSuccessfully
        """
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response = self.client.post(
            '/api/v1/booking', headers=dict(Authorization="Bearer " + access_token), data=json.dumps(
                dict(flight_id=1)), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)

    def test_booking_full_flight(self):
        """
        Test booking a flight Successfully
        """
        flight = Flight(
            flight_name='Kenya Airways', flight_number='KQ-13',
            flight_date=datetime(2019, 3, 3, 10, 10, 10),
            flight_destination='Kampala', capacity=1)
        flight.save()
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response11 = self.client.post(
            '/api/v1/booking', headers=dict(Authorization="Bearer " + access_token), data=json.dumps(
                dict(flight_id=1)), content_type='application/json')
        response = self.client.post(
            '/api/v1/booking', headers=dict(Authorization="Bearer " + access_token), data=json.dumps(
                dict(flight_id=1)), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)
