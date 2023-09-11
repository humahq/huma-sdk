import unittest
import huma_sdk
import os
from bson import ObjectId
import time
from huma_sdk.utils._log_utils import get_logger


class TestQuestionsClientIntegration(unittest.TestCase):

    def setUp(self):
        self.logger = get_logger(__name__)
        self.question = "Top sponsors in nsclc"
        self.commands = []
        self.page, self.limit = 1, 20
        self.expected_questions_status = ("succeeded", "processing", "accepted", "rejected")
        self.expected_answer_keys = ('type', "data")
        self.status_message = {
            "accepted": 'Question accepted successfully', 
            "rejected": "Question rejected  due to an error, please try again"
        }
        self.questions_client = huma_sdk.session(service_name="Questions", api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))

    def assert_submission_result(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        submission_status = result['question_status']
        self.assertIn(submission_status, self.expected_questions_status)

        message_status = result['message']
        self.assertEqual(message_status, self.status_message[submission_status])

        ticket_number = result['ticket_number']
        assert ObjectId(ticket_number)

    def assert_question_status_result(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("question_status", result)
        submission_status = result['question_status']
        self.assertIn(submission_status, self.expected_questions_status)

        self.assertIn("ticket_number", result)
        ticket_number = result['ticket_number']
        self.assertEqual(ticket_number, self.ticket_number)
    
    def assert_answer(self, result):
        self.assertTrue(result)
        self.assertIsInstance(result, dict)

        self.assertIn("answer", result)
        answer = result['answer']
        if answer:
            for key in self.expected_answer_keys:
                self.assertIn(key, answer)

    def fetch_answer(self):
        self.logger.info('Initializing Test:  fetch_answer')
        result = self.questions_client.fetch_answer(ticket_number=self.ticket_number, page=self.page, limit=self.limit)
        self.assert_answer(result)
        self.logger.info('Completed Test:  fetch_answer')

    def check_question_status(self, question_status):
        self.logger.info('Initializing Test:  check_question_status')
        while question_status not in ('succeeded', "rejected"):
            self.logger.info(f'Processing Test:  check_question_status, waiting for status "{question_status}" to get succeeded or rejected')
            time.sleep(5)
            result = self.questions_client.check_question_status(ticket_number=self.ticket_number)
            self.assert_question_status_result(result)
            question_status = result['question_status']

        self.logger.info('Completed Test:  check_question_status')
        return question_status

    def submit_question(self):
        self.logger.info('Initializing Test:  submit_question')
        result = self.questions_client.submit_question(question=self.question, commands=self.commands)
        self.assert_submission_result(result)
        self.ticket_number = result['ticket_number']
        self.logger.info('Completed Test:  submit_question')
        return result['question_status']

    def test_questions_success(self):
        question_status = self.submit_question()
        question_status = self.check_question_status(question_status)
        if question_status == "succeeded":
            self.fetch_answer()


if __name__ == '__main__':
    import nose2
    nose2.discover()
