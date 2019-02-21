import json

from tests import BaseTestCase


class TestBooking(BaseTestCase):

    def test_booking_flight_successfully(self):
        """
        Test booking a flight Successfully
        """
        self.create_flight(20)
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
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
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)

    def test_booking_flight_without_required_input(self):
        """
        Test booking a flight unSuccessfully
        """
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict()),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)

    def test_booking_full_flight(self):
        """
        Test booking a flight Successfully
        """
        self.create_flight(1)
        response1 = self.register_user('test@gmail.com', 'tesTing123', 'test')
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response11 = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
        response = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'fail')
        self.assertEqual(response.status_code, 400)

    def test_viewing_reserved_flights(self):
        """
        Test viewing reserved flights
        """
        self.create_flight(20)
        self.create_admin_user()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response11 = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
        response = self.client.get(
            '/api/v1/booking/daily',
            headers=dict(Authorization="Bearer " + access_token),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

    def test_unathourized_viewing_reserved_flights(self):
        """
        Test unauthorized viewing reserved flights
        """
        self.create_flight(20)
        self.create_user()
        response2 = self.login_user('test@gmail.com', 'tesTing123')
        access_token = json.loads(response2.data.decode())['auth_token']

        response11 = self.client.post(
            '/api/v1/booking',
            headers=dict(Authorization="Bearer " + access_token),
            data=json.dumps(dict(flight_id=1)),
            content_type='application/json'
        )
        response = self.client.get(
            '/api/v1/booking/daily',
            headers=dict(Authorization="Bearer " + access_token),
            content_type='application/json'
        )
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
