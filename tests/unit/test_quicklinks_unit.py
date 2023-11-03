import unittest
from bson import ObjectId
from unittest.mock import patch
from huma_sdk._services._quicklinks import _Quicklinks


class TestFetchQuicklinksUnitCase(unittest.TestCase):

    def create_expected_response_payload(self):
        return {
            "categories": [{
                "title": "",
                "suggestions": []
            }]
        }

    def assert_result(self, quicklinks_payload, expected_response):
        self.assertEqual(quicklinks_payload, expected_response)

    @patch.object(_Quicklinks, '_make_request')
    def test_fetch_quicklinks_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Quicklinks()
        quicklinks_payload = client.fetch_quicklinks()
        self.assert_result(quicklinks_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
