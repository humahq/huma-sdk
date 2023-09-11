import unittest
import huma_sdk
import os
from bson import ObjectId
from huma_sdk.utils._log_utils import get_logger


class TestFavoritesClientIntegration(unittest.TestCase):

    def setUp(self):
        self.logger = get_logger(__name__)
        self.expected_favorite_object_keys = ('type', "question", "ticket_number", "thumbnail")
        self.expected_answer_keys = ('data', 'type')
        self.favorites_client = huma_sdk.session(service_name="Favorites", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_favorites(self,result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("favorites", result)
        favorite = result['favorites']
        if favorite:
            favorite_object = favorite[0]
            for key in self.expected_favorite_object_keys:
                self.assertIn(key, favorite_object)

            ticket_number = favorite_object['ticket_number']
            assert ObjectId(ticket_number)
            visual_types = favorite_object['type']
            self.assertIsInstance(visual_types, str)

    def assert_favorite_data(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("answer", result)
        answer = result['answer']
        if answer:
            response_visual_type = answer['type']
            self.assertEqual(self.visual_type, response_visual_type)
            for key in self.expected_answer_keys:
                self.assertIn(key, answer)

    def assert_create_favorite(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("data", result)
        result = result['data']

        self.assertIn("favorite", result)
        favorite = result['favorite']

        self.assertIn("ticket_number", favorite)
        ticket_number = favorite['ticket_number']
        self.assertEqual(ticket_number, self.ticket_number)
        for key in self.expected_favorite_object_keys:
            if key != "type":
                self.assertIn(key, favorite)

    def fetch_favorites(self):
        result = self.favorites_client.fetch_favorites(page=1, limit=20, sort_by="created_date", order_by=-1, question="")
        self.assert_favorites(result)
        favorite_object = result['favorites'][0]
        self.ticket_number = favorite_object['ticket_number']
        self.visual_type = favorite_object['type']

    def fetch_favorite_data(self):
        result = self.favorites_client.fetch_favorite_data(ticket_number=self.ticket_number, page=1, limit=20, type=self.visual_type)
        self.assert_favorite_data(result)

    def delete_favorite(self):
        result = self.favorites_client.delete_favorite(ticket_number=self.ticket_number)
        self.assertFalse(result)

    def create_favorite(self):
        result = self.favorites_client.create_favorite(ticket_number=self.ticket_number)
        self.assert_create_favorite(result)

    def test_histories_module(self):
        self.fetch_favorites()
        self.fetch_favorite_data()
        self.delete_favorite()
        self.create_favorite()


if __name__ == '__main__':
    import nose2
    nose2.discover()
