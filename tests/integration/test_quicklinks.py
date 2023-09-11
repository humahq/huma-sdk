import unittest
import huma_sdk
import os

class TestQuicklinksClientIntegration(unittest.TestCase):

    def setUp(self):
        self.quicklinks_client = huma_sdk.session(service_name="Quicklinks", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_results(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn('categories', result)

        quicklinks = result['categories']
        self.assertIsInstance(quicklinks, list)

        if quicklinks:
            quicklink = quicklinks[0]
            self.assertIn('suggestions', quicklink)


    def test_fetch_quicklinks_success(self):
        result = self.quicklinks_client.fetch_quicklinks()
        self.assert_results(result)


if __name__ == '__main__':
    import nose2
    nose2.discover()
