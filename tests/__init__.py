import json

from datetime import datetime
from flask_testing import TestCase

from app import app, db, app_configuration
from app.models import Flight, User


class BaseTestCase(TestCase):
    """
    Base test class
    """

    def create_app(self):
        app.config.from_object(app_configuration['testing'])
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def register_user(self, email=None, password=None, name=None, role=False):
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(
                dict(email=email, password=password, name=name)),
            content_type='application/json',
        )

    def login_user(self, email=None, password=None):
        return self.client.post(
            '/api/v1/auth/login',
            data=json.dumps(dict(email=email, password=password)),
            content_type='application/json',
        )

    def create_user(self):
        user = User(email='test@gmail.com',
                    password='tesTing123', name='test')
        user.save()

    def create_flight(self, capacity):
        flight = Flight(
            flight_name='Kenya Airways', flight_number='KQ-13',
            flight_date=datetime(2019, 3, 3, 10, 10, 10),
            flight_destination='Kampala', capacity=capacity
        )
        flight.save()

    def create_admin_user(self):
        user = User(email='test@gmail.com',
                    password='tesTing123', name='test', role=True)
        user.save()
