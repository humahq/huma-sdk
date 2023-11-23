import unittest
import huma_sdk
import os
import random
from bson import ObjectId
import time


class TestHistoriesClientIntegration(unittest.TestCase):

    def setUp(self):
        self.file_type = "pdf"
        self.expected_history_object_keys = ('type', "question", "ticket_number", "possible_types", "type", "thumbnail")
        self.expected_answer_keys = ('data', 'type')
        self.expected_history_status = ("succeeded", "processing", "accepted", "rejected")
        self.histories_client = huma_sdk.session(service_name="Histories", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_history(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("histories", result)
        history = result['histories']
        if history:
            history_object = history[0]
            for key in self.expected_history_object_keys:
                self.assertIn(key, history_object)

            ticket_number = history_object['ticket_number']
            assert ObjectId(ticket_number)
            possible_types = history_object['possible_types']
            self.assertIsInstance(possible_types, list)


    def assert_history_data(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("answer", result)
        answer = result['answer']
        if answer:
            visual_type = answer['type']
            self.assertEqual(self.expected_visual_type, visual_type)
            for key in self.expected_answer_keys:
                self.assertIn(key, answer)

    def assert_submit_history_visual(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("status", result)
        submission_status = result['status']
        self.assertIn(submission_status, self.expected_history_status)

        self.assertIn("conversion_id", result)
        conversion_id = result['conversion_id']
        assert ObjectId(conversion_id)

    def assert_check_history_visual_status(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        submission_status = result['status']
        self.assertIn(submission_status, self.expected_history_status)

        conversion_id = result['conversion_id']
        assert ObjectId(conversion_id)
        self.assertEqual(conversion_id, self.conversion_id)

    def assert_fetch_history_visual_result(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)
        self.assertIn('download_url', result)

    def get_history_object(self, is_batch_pages=True):
        histories_client = huma_sdk.session(service_name="Histories", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

        if is_batch_pages:
            result = histories_client.fetch_history(page=1, limit=20, sort_by="created_data", order_by=-1, question="")
        else:
            result = histories_client.fetch_history(limit=20, sort_by="created_data", order_by=-1, question="", is_batch_pages=True, max_page_count=5)

        if not isinstance(result, dict) or not result.get('histories'):
            return []
        result['histories'] = [history for history in result['histories'] if 'type' in history]
        return result if result['histories'] else []

    def fetch_history(self):
        result = self.get_history_object()
        if result:
            self.assert_history(result)
            history_object = result['histories'][0]
            self.ticket_number = history_object['ticket_number']
            self.possible_types = history_object['possible_types']
        return result

    def fetch_aggregated_history(self):
        result = self.get_history_object(is_batch_pages=True)
        if result:
            self.assert_history(result)
            history_object = result['histories'][0]
            self.ticket_number = history_object['ticket_number']
            self.possible_types = history_object['possible_types']
        return result

    def fetch_history_data(self):
        type = random.choice(self.possible_types) if self.possible_types else ""
        result = self.histories_client.fetch_history_data(ticket_number=self.ticket_number, page=1, limit=20, type=type)
        self.expected_visual_type = type
        self.assert_history_data(result)

    def fetch_aggregated_history_data(self):
        type = random.choice(self.possible_types) if self.possible_types else ""
        result = self.histories_client.fetch_history_data(ticket_number=self.ticket_number, limit=20, type=type, is_batch_pages=True, max_page_count=5)
        self.expected_visual_type = type
        self.assert_history_data(result)

    def submit_history_visual(self)-> str:
        visual_type = random.choice(self.possible_types) if self.possible_types else ""
        result = self.histories_client.submit_history_visual(ticket_number=self.ticket_number, file_type=self.file_type, visual_type=visual_type)
        self.assert_submit_history_visual(result)
        self.conversion_id = result['conversion_id']
        return result['status']

    def check_history_visual_status(self, status: str)-> str:
        while status not in ('succeeded', "rejected"):
            time.sleep(5)
            result = self.histories_client.check_history_visual_status(self.conversion_id)
            self.assert_check_history_visual_status(result)
            status = result['status']

        return status

    def fetch_history_visual_result(self):
        result = self.histories_client.fetch_history_visual_result(self.conversion_id)
        self.assert_fetch_history_visual_result(result)

    def test_histories_module(self):
        result = self.fetch_history()
        if result:
            self.fetch_history_data()
            self.fetch_aggregated_history_data()
            status = self.submit_history_visual()
            status = self.check_history_visual_status(status)
            if status == "succeeded":
                self.fetch_history_visual_result()


if __name__ == '__main__':
    import nose2
    nose2.discover()
