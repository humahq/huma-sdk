import unittest
from unittest.mock import patch
from huma_sdk._services._audits import _Audits


class TestFetchAliasesUnitCase(unittest.TestCase):

    def setUp(self):
        self.keyword_paramaters = dict(page=1, limit=50, sort_by=-1, order_by="", endpoint="", content="")
        self.aggregated_keyword_paramaters = dict(limit=50, sort_by=-1, order_by="", endpoint="", content="", is_batch_pages=True, max_page_count=5)

    def create_expected_response_payload(self):
        return {
            "audit_trail": [
                {
                    "content": "",
                    "context": None,
                    "created": 1693544936046,
                    "customer": "",
                    "endpoint": "",
                    "user_email": "",
                    "environment": ""
                },
            ]
        }

    def assert_result(self, audits_payload, expected_response):
        self.assertEqual(audits_payload, expected_response)

    @patch.object(_Audits, '_make_request')
    def test_fetch_audits_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Audits()
        audits_payload = client.fetch_audits(**self.keyword_paramaters)
        self.assert_result(audits_payload, expected_response)

    @patch.object(_Audits, '_make_request')
    def test_fetch_aggregated_audits_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Audits()
        audits_payload = client.fetch_audits(**self.aggregated_keyword_paramaters)
        self.assert_result(audits_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()