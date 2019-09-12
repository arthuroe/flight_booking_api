from flask_testing import TestCase

from app import app, app_configuration


class TestProductionConfig(TestCase):
    """
    Test the production configuration
    """

    def create_app(self):
        app.config.from_object(app_configuration['production'])
        return app

    def test_app_is_running_on_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is 'ArandomText')


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
        url = 'sqlite:///flight_testing_db'
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] == url)


class TestDevelopmentConfig(TestCase):
    """
    Test the development configuration
    """

    def create_app(self):
        app.config.from_object(app_configuration['development'])
        return app

    def test_app_is_running_on_development(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['SECRET_KEY'] is 'ArandomText')
        self.assertTrue(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False)
        self.assertTrue(app.config['SQLALCHEMY_ECHO'] is False)
