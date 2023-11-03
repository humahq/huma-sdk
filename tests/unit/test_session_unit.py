import unittest
from bson import ObjectId
from unittest.mock import patch, MagicMock
from huma_sdk._session import _Session


class TestFetchQuicklinksUnitCase(unittest.TestCase):

    def create_expected_response_payload(self):
        return MagicMock()

    def assert_result(self, service_client, expected_response):
        self.assertEqual(service_client, expected_response)

    @patch.object(_Session, 'create_connection')
    def test_fetch_quicklinks_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Session(service_name="Questions")
        service_client = client.create_connection()
        self.assert_result(service_client, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
