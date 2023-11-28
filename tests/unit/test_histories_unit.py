import unittest
from bson import ObjectId
from unittest.mock import patch
from huma_sdk._services._histories import _Histories


class TestFetchHistoryUnitCase(unittest.TestCase):

    def setUp(self):
        self.keyword_paramaters = dict(page=1, limit=20, sort_by=-1, order_by="", question="")
        self.aggregated_keyword_parameters = dict(limit=50, sort_by=-1, order_by="", question="", is_batch_pages=True, max_page_count=5)

    def create_expected_response_payload(self):
        return {
            "history":[{
                "type": "",
                "question":"",
                "thumbnail":"",
                "initial_type":"",
                "possibleTypes":[],
                "ticket_number":""
            }]
        }

    def assert_result(self, histories_payload, expected_response):
        self.assertEqual(histories_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_fetch_history_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        histories_payload = client.fetch_history(**self.keyword_paramaters)
        self.assert_result(histories_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_fetch_aggregated_history_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        histories_payload = client.fetch_history(**self.aggregated_keyword_parameters)
        self.assert_result(histories_payload, expected_response)


class TestFetchHistoryDataUnitCase(unittest.TestCase):

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

    def assert_result(self, history_payload, expected_response):
        self.assertEqual(history_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_fetch_history_data_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        history_payload = client.fetch_history_data(self.mock_ticket_number, page=1, limit=50)
        self.assert_result(history_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_fetch_aggregated_history_data_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        history_payload = client.fetch_history_data(self.mock_ticket_number, limit=50, is_batch_pages=True, max_page_count=5)
        self.assert_result(history_payload, expected_response)


class TestSubmitHistoryVisualUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_conversion_id = str(ObjectId())
        self.mock_ticket_number = str(ObjectId())
        self.payload =self.payload ={
            "ticket_number": self.mock_ticket_number,
            "file_type":"pdf"
        }

    def create_expected_response_payload(self):
        return {
            "status": "accepted",
            "file_type": "pdf",
            "visual_type": "bar_chart",
            "conversion_id": self.mock_conversion_id
        }

    def assert_result(self, submission_payload, expected_response):
        self.assertEqual(submission_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_submit_history_visual_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        submission_payload = client.submit_history_visual(**self.payload)
        self.assert_result(submission_payload, expected_response)


class TestCheckHistoryVisualStatusUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_conversion_id = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "status": "accepted",
            "file_type": "pdf",
            "visual_type": "bar_chart",
            "conversion_id": self.mock_conversion_id
        }

    def assert_result(self, history_payload, expected_response):
        self.assertEqual(history_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_check_history_visual_status_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        history_payload = client.check_history_visual_status(self.mock_conversion_id)
        self.assert_result(history_payload, expected_response)


class TestFetchHistoryVisualResultUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_conversion_id = str(ObjectId())
        self.mock_url = "https://mock.example/download_url"

    def create_expected_response_payload(self):
        return {
            "download_url": self.mock_url,
            "file_type": "pdf",
            "visual_type": "bar_chart"
        }

    def assert_result(self, submission_payload, expected_response):
        self.assertEqual(submission_payload, expected_response)

    @patch.object(_Histories, '_make_request')
    def test_fetch_history_visual_result_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Histories()
        history_payload = client.fetch_history_visual_result(self.mock_conversion_id)
        self.assert_result(history_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
