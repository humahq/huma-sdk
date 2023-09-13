import unittest
import huma_sdk
import os
from bson import ObjectId


class TestSubscriptionsClientIntegration(unittest.TestCase):

    def setUp(self):
        self.expected_subscribe_object_keys = ("question", "subscribed_id", "thumbnail")
        self.expected_answer_keys = ('data', 'type')
        self.subscriptions_client = huma_sdk.session(service_name="Subscriptions", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_subscriptions(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscriptions", result)
        subscribe = result['subscriptions']
        if subscribe:
            subscribe_object = subscribe[0]
            for key in self.expected_subscribe_object_keys:
                self.assertIn(key, subscribe_object)

            subscribed_id = subscribe_object['subscribed_id']
            assert ObjectId(subscribed_id)
            question = subscribe_object['question']
            self.assertIsInstance(question, str)

    def assert_subscription_data(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscriptions", result)
        answer = result['subscriptions']
        if answer:
            for key in self.expected_answer_keys:
                self.assertIn(key, answer)

    def assert_assert_subscription_status(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("is_subscribed", result)
        is_subscribed = result['is_subscribed']

        self.assertTrue(is_subscribed)

    def assert_create_subscription(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscribed_id", result)
        subscribed_id = result['subscribed_id']

        if result:
            for key in self.expected_subscribe_object_keys:
                self.assertIn(key, result)

    def get_history(self):
        histories_client = huma_sdk.session(service_name="Histories", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))
        page, limit = 1, 20
        while True:
            result = histories_client.fetch_history(page=page, limit=limit, sort_by="created_data", order_by=-1, question="")
            if not isinstance(result, dict) or not result.get('histories'):
                return []
            for history in result['histories']:
                if 'type' in history:
                    self.ticket_number = history['ticket_number']
                    return
            page += 1

    def handle_empty_subscription(self):
        result = self.get_history()
        if result:
            self.create_subscription()
            self.fetch_subscriptions()
        return result
    
    def fetch_subscriptions(self):
        result = self.subscriptions_client.fetch_subscriptions(page=1, limit=20, sort_by="created_date", order_by=-1, question="")
        if not result.get('subscriptions'):
            result = self.handle_empty_subscription()
            if not result:
                return result
        else:
            self.assert_subscriptions(result)
            subscribe_object = result['subscriptions'][0]
            self.subscribed_id = subscribe_object['subscribed_id']
            self.question = subscribe_object['question']
            return result

    def fetch_subscription_data(self):
        result = self.subscriptions_client.fetch_subscription_data(subscribed_id=self.subscribed_id, page=1, limit=20)
        self.assert_subscription_data(result)

    def delete_subscription(self):
        result = self.subscriptions_client.delete_subscription(subscribed_id=self.subscribed_id)
        self.assertFalse(result)

    def fetch_subscription_status(self):
        result = self.subscriptions_client.fetch_subscription_status(question=self.question)
        self.assert_assert_subscription_status(result)

    def create_subscription(self):
        result = self.subscriptions_client.create_subscription(ticket_number = self.ticket_number)
        self.assert_create_subscription(result)

    def test_histories_module(self):
        result = self.fetch_subscriptions()
        if result:
            self.fetch_subscription_data()
            self.fetch_subscription_status()
            self.delete_subscription()


if __name__ == '__main__':
    import nose2
    nose2.discover()
