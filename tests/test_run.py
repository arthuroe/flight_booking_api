from tests import BaseTestCase


class TestRun(BaseTestCase):
    def test_app_get(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_app_get404(self):
        response = self.client.get('/unknown')
        self.assert404(response)


from app import app, app_configuration
from flask_testing import TestCase


class TestProductionConfig(TestCase):
    """
    Test the production configuration
    """

    def create_app(self):
        app.config.from_object(app_configuration['production'])
        return app

    def test_app_is_running_on_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'averyrandomstringthatshardtodecode')


class TestTestingConfig(TestCase):
    """
    Test the testing configuration
    """

    def create_app(self):
        app.config.from_object(app_configuration['testing'])
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'])
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            'sqlite:///flight_testing_db'
        )


class TestDevelopmentConfig(TestCase):
    """
    Test the development configuration
    """

    def create_app(self):
        app.config.from_object(app_configuration['development'])
        return app

    def test_app_is_running_on_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is
                         'averyrandomstringthatshardtodecode')
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False)
        self.assertTrue(app.config['SQLALCHEMY_ECHO'] is False)
