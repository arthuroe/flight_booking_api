import json

from tests import BaseTestCase


class TestFlight(BaseTestCase):

    def test_viewing_available_flights(self):
        """
        Test to see available flights
        """
        response1 = self.register_user('test', 'testing', 'test')
        response2 = self.login_user('test', 'testing')
        access_token = json.loads(response2.data.decode())['auth_token']
        response = self.client.get(
            '/api/v1/flights', headers=dict(Authorization="Bearer " + access_token,
                                            content_type='application/json'))
        result = json.loads(response.data.decode())
        self.assertTrue(result['status'] == 'success')
        self.assertEqual(response.status_code, 200)
