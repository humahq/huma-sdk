import unittest
from bson import ObjectId
from unittest.mock import patch
from huma_sdk._services._questions import _Questions


class TestSubmitQuestionUnitCase(unittest.TestCase):

    def setUp(self):
        self.payload = {
            "question": "Top Sponsors in NSCLC",
            "commands": ["no answer cache"],
        }
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "message": "Question accepted successfully",
            "question_status": "accepted",
            "question": "Top Sponsors in NSCLC",
            "ticket_number": self.mock_ticket_number
        }

    def assert_result(self, submission_payload, expected_response):
        self.assertEqual(submission_payload, expected_response)

    @patch.object(_Questions, '_make_request')
    def test_submit_question_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Questions()
        submission_payload = client.submit_question(**self.payload)
        self.assert_result(submission_payload, expected_response)


class TestCheckQuestionStatusUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "question": "Planned patient enrollment for pediatric ewing's sarcoma trials",
            "question_status": "accepted",
            "ticket_number": self.mock_ticket_number
        }

    def assert_result(self, question_payload, expected_response):
        self.assertEqual(question_payload, expected_response)

    @patch.object(_Questions, '_make_request')
    def test_check_question_status_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Questions()
        question_payload = client.check_question_status(self.mock_ticket_number)
        self.assert_result(question_payload, expected_response)


class TestGetAnswerUnitCase(unittest.TestCase):

    def setUp(self):
        self.mock_ticket_number = str(ObjectId())

    def create_expected_response_payload(self):
        return {
            "answer":{
                "data":[],
                "type":"table"
            },
            "question": "Top Sponsors in NSCLC",
            "ticket_number": self.mock_ticket_number,
            "altered_question":"Top Sponsors in NSCLC"
        }

    def assert_result(self, answer_payload, expected_response):
        self.assertEqual(answer_payload, expected_response)

    @patch.object(_Questions, '_make_request')
    def test_get_answer_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Questions()
        answer_payload = client.fetch_answer(self.mock_ticket_number,  page=1, limit=50)
        self.assert_result(answer_payload, expected_response)

    @patch.object(_Questions, '_make_request')
    def test_get_aggregated_answer_success(self, mock_make_request):
        expected_response = self.create_expected_response_payload()
        mock_make_request.return_value = expected_response
        client = _Questions()
        answer_payload = client.fetch_answer(self.mock_ticket_number, limit=50, is_batch_pages=True, max_page_count=5)
        self.assert_result(answer_payload, expected_response)


if __name__ == '__main__':
    import nose2
    nose2.discover()
