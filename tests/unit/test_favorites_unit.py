import unittest
from bson import ObjectId
from unittest.mock import patch
from huma_sdk._services._favorites import _Favorites


class TestFetchFavoritesUnitCase(unittest.TestCase):

    def setUp(self):
        self.keyword_paramaters = dict(page=1, limit=50, sort_by=-1, order_by="", question="")

    def create_expected_response_payload(self):
        return {
            "favorites":[
                {
                    "question": "",
                    "thumbnail":"",
                    "ticket_number":"",
                    "type":""
                }
            ]
        }

    def assert_result(self, favorites_payload, expected_response):
        self.assertEqual(favorites_payload, expected_response)

    @patch.object(_Favorites, '_make_request')
    def test_submit_question_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Favorites()
        favorites_payload = client.fetch_favorites(**self.keyword_paramaters)
        self.assert_result(favorites_payload, expected_response)


class TestCreateFavoriteUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())
        self.payload = {
            "ticket_number": f'{self.mock_ticket_number}',
        }

    def create_expected_response_payload(self):
        return {
            "favorites": {
                "question": "Top sponsors in nsclc",
                "thumbnail":"",
                "ticket_number": self.mock_ticket_number,
            }
        }

    def assert_result(self, favorite_payload, expected_response):
        self.assertEqual(favorite_payload, expected_response)

    @patch.object(_Favorites, '_make_request')
    def test_create_favorite_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Favorites()
        favorite_payload = client.create_favorite(self.mock_ticket_number)
        self.assert_result(favorite_payload, expected_response)


class TestFetchFavoriteDataUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "answer":{
                "data":[],
                "type":""
            },
            "question": "",
            "ticket_number": self.mock_ticket_number
        }

    def assert_result(self, favorite_payload, expected_response):
        self.assertEqual(favorite_payload, expected_response)

    @patch.object(_Favorites, '_make_request')
    def test_fetch_favorite_data_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Favorites()
        favorite_payload = client.fetch_favorite_data(self.mock_ticket_number)
        self.assert_result(favorite_payload, expected_response)


class TestDeleteFavoritesUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "answer":{
                "data":[],
                "type":""
            },
            "question": "",
            "ticket_number": self.mock_ticket_number
        }

    def assert_result(self, favorite_payload):
        self.assertIsNone(favorite_payload)

    @patch.object(_Favorites, '_make_request')
    def test_delete_favorite_success(self, mock_make_request):
        mock_make_request.return_value = None
        client = _Favorites()
        favorite_payload = client.delete_favorite(self.mock_ticket_number)
        self.assert_result(favorite_payload)


if __name__ == '__main__':
    import nose2
    nose2.discover()
