import unittest
import huma_sdk
import os

class TestAliasClientIntegration(unittest.TestCase):

    def setUp(self):
        self.aliases_client = huma_sdk.session(service_name="Aliases", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))
        self.required_params_test_1 = dict(page=1, limit=20, sort_by=-1, order_by="", search_by="", search_for="")
        self.required_params_test_2 = dict(page=1, limit=20, sort_by=-1, order_by="created_date", search_for="", search_by="", is_batch_pages=True, max_page_count=5)
        self.expected_keys = ("_id","type", "rule_name", "rule_type")

    def assert_results(self, result):
        self.assertIsInstance(result, dict)
        self.assertIn('aliases', result)

        aliases = result['aliases']
        self.assertIsInstance(aliases, list)

        if not self.required_params.get('is_batch_pages'):
            self.assertTrue(len(aliases)<=self.required_params['limit'])

        returned_keys = aliases[0].keys() if aliases else []
        if returned_keys:
            for key in self.expected_keys:
                self.assertIn(key, returned_keys)

    def test_fetch_aliases_success(self):
        self.required_params = self.required_params_test_1
        result = self.aliases_client.fetch_aliases(**self.required_params)
        self.assert_results(result)

    def test_aggregated_fetch_aliases_success(self):
        self.required_params = self.required_params_test_2
        result = self.aliases_client.fetch_aliases(**self.required_params)
        self.assert_results(result)


if __name__ == '__main__':
    import nose2
    nose2.discover()
