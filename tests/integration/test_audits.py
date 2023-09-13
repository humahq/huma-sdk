import unittest
import huma_sdk
import os

class TestAuditsClientIntegration(unittest.TestCase):

    def setUp(self):
        self.audits_client = huma_sdk.session(service_name="Audits", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))
        self.required_params = dict()
        self.expected_keys = ("environment", "user_email", "content", "endpoint", "customer")

    def assert_results(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn('audit_trail', result)

        audits = result['audit_trail']
        self.assertIsInstance(audits, list)
        if self.required_params.get('limit'):
            self.assertTrue(len(audits)<=self.required_params['limit'])

        returned_keys = audits[0].keys() if audits else []
        if returned_keys:
            for key in self.expected_keys:
                self.assertIn(key, returned_keys)

    def test_fetch_audits_success(self):
        result = self.audits_client.fetch_audits(**self.required_params)
        self.assert_results(result)


if __name__ == '__main__':
    import nose2
    nose2.discover()
