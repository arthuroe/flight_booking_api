from tests import BaseTestCase


class TestRun(BaseTestCase):
    def test_app_get(self):
        response = self.client.get('/')
        self.assert200(response)

    def test_app_get404(self):
        response = self.client.get('/unknown')
        self.assert404(response)
