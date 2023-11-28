import unittest
from bson import ObjectId
from unittest.mock import patch
from huma_sdk._services._subscriptions import _Subscriptions


class TestFetchSubscriptionsUnitCase(unittest.TestCase):

    def setUp(self):
        self.keyword_paramaters = dict(page=1, limit=20, sort_by=-1, order_by="", question="")
        self.aggregated_keyword_parameters = dict(limit=20, sort_by=-1, order_by="", question="", is_batch_pages=True, max_page_count=5)

    def create_expected_response_payload(self):
        return {
            "subscriptions":[
                {
                    "question": "",
                    "thumbnail":"",
                    "subscribed_id":""
                }
            ]
        }

    def assert_result(self, subscription_payload, expected_response):
        self.assertEqual(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_fetch_subscriptions_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.fetch_subscriptions(**self.keyword_paramaters)
        self.assert_result(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_fetch_aggregated_subscriptions_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.fetch_subscriptions(**self.aggregated_keyword_parameters)
        self.assert_result(subscription_payload, expected_response)


class TestCreateSubscriptionUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "favorites": {
                "question": "Top sponsors in nsclc",
                "thumbnail":"",
                "ticket_number": self.mock_ticket_number,
            }
        }

    def assert_result(self, subscription_payload, expected_response):
        self.assertEqual(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_create_subscription_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.create_subscription(self.mock_ticket_number)
        self.assert_result(subscription_payload, expected_response)


class TestFetchSubscriptionDataUnitCase(unittest.TestCase):

    def setUp(self):
        self.subscribed_id = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "answer":{
                "data":[],
                "type":""
            },
            "question": "",
            "subscribed_id": self.subscribed_id
        }

    def assert_result(self, subscription_payload, expected_response):
        self.assertEqual(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_fetch_subscription_data_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.fetch_subscription_data(self.subscribed_id, page=1, limit=50)
        self.assert_result(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_fetch_aggregated_subscription_data_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.fetch_subscription_data(self.subscribed_id, limit=50, is_batch_pages=True, max_page_count=5)
        self.assert_result(subscription_payload, expected_response)


class TestDeleteSubscriptionUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def assert_result(self, subscription_payload):
        self.assertIsNone(subscription_payload)

    @patch.object(_Subscriptions, '_make_request')
    def test_delete_subscription_success(self, mock_make_request):
        mock_make_request.return_value = None
        client = _Subscriptions()
        subscription_payload = client.delete_subscription(self.mock_ticket_number)
        self.assert_result(subscription_payload)


class TestFetchSubscriptionStatusUnitCase(unittest.TestCase):

    def setUp(self):
        self.question = "Top sponsors in nsclc"

    def create_expected_response_payload(self):
        return { "is_subscribed": True }

    def assert_result(self, subscription_payload, expected_response):
        self.assertEqual(subscription_payload, expected_response)

    @patch.object(_Subscriptions, '_make_request')
    def test_fetch_subscription_status_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Subscriptions()
        subscription_payload = client.fetch_subscription_status(self.question)
        self.assert_result(subscription_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
