import unittest
import huma_sdk
import os
from bson import ObjectId


class TestSubscribesClientIntegration(unittest.TestCase):

    def setUp(self):
        self.expected_subscribe_object_keys = ("question", "subscribed_id", "thumbnail")
        self.expected_answer_keys = ('data', 'type')
        self.subscribes_client = huma_sdk.session(service_name="Subscriptions", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_subscribes(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscribes", result)
        subscribe = result['subscribes']
        if subscribe:
            subscribe_object = subscribe[0]
            for key in self.expected_subscribe_object_keys:
                self.assertIn(key, subscribe_object)

            subscribed_id = subscribe_object['subscribed_id']
            assert ObjectId(subscribed_id)
            question = subscribe_object['question']
            self.assertIsInstance(question, str)

    def assert_subscribe_data(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscribes", result)
        answer = result['subscribes']
        if answer:
            for key in self.expected_answer_keys:
                self.assertIn(key, answer)

    def assert_assert_subscribed_status(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("is_subscribed", result)
        is_subscribed = result['is_subscribed']

        self.assertTrue(is_subscribed)

    def assert_create_subscribe(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("subscribed_id", result)
        subscribed_id = result['subscribed_id']

        if result:
            for key in self.expected_subscribe_object_keys:
                self.assertIn(key, result)

    def get_history(self):
        histories_client = huma_sdk.session(service_name="Histories", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))
        result =  histories_client.fetch_history(page=1, limit=20, sort_by="created_data", order_by=-1, question="")
        history_object = result['histories'][0]
        self.ticket_number = history_object['ticket_number']

    def handle_empty_subscribe(self):
        self.get_history()
        self.create_subscribe()
        self.fetch_subscribes()
    
    def fetch_subscribes(self):
        result = self.subscribes_client.fetch_subscription(page=1, limit=20, sort_by="created_date", order_by=-1, question="")
        if not result.get('subscribes'):
            self.handle_empty_subscribe()
        else:
            self.assert_subscribes(result)
            subscribe_object = result['subscribes'][0]
            self.subscribed_id = subscribe_object['subscribed_id']
            self.question = subscribe_object['question']

    def fetch_subscribe_data(self):
        result = self.subscribes_client.fetch_subscription_data(subscribed_id=self.subscribed_id, page=1, limit=20)
        self.assert_subscribe_data(result)

    def delete_subscribe(self):
        result = self.subscribes_client.delete_subscription(subscribed_id=self.subscribed_id)
        self.assertFalse(result)

    def fetch_subscribed_status(self):
        result = self.subscribes_client.fetch_subscription_status(question=self.question)
        self.assert_assert_subscribed_status(result)

    def create_subscribe(self):
        result = self.subscribes_client.create_subscription(ticket_number = self.ticket_number)
        self.assert_create_subscribe(result)

    def test_histories_module(self):
        self.fetch_subscribes()
        self.fetch_subscribe_data()
        self.fetch_subscribed_status()
        self.delete_subscribe()


if __name__ == '__main__':
    import nose2
    nose2.discover()
