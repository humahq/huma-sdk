import unittest
from unittest.mock import patch
from huma_sdk._services._aliases import _Aliases


class TestFetchAliasesUnitCase(unittest.TestCase):
    def setUp(self):
        self.keyword_parameters = dict(page=1, limit=50, sort_by=-1, order_by="", search_by="", search_for="")

    def create_expected_response_payload(self):
        return {
            "aliases": [{
                "type": "",
                "scope": "",
                "rule_name": "",
                "rule_type": "",
            }]
        }

    def assert_result(self, aliases_payload, expected_response):
        self.assertEqual(aliases_payload, expected_response)

    @patch.object(_Aliases, '_make_request')
    def test_fetch_aliases_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Aliases()
        aliases_payload = client.fetch_aliases(**self.keyword_parameters)
        self.assert_result(aliases_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
