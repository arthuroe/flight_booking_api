import json

from flask_testing import TestCase
from app import app, db, app_configuration


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

    def register_user(self, username=None, password=None, name=None):
        return self.client.post(
            '/api/v1/auth/register',
            data=json.dumps(dict(
                username=username,
                password=password,
                name=name
            )),
            content_type='application/json',
        )
