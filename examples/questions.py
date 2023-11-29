import json
import os
import time
import sys

import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

class HumaSDKQuestionsClient:
    def __init__(self, service_name):
        self.questions_client = huma_sdk.session(service_name=service_name)

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def submit_question(self, question: str="", commands: list=None):
        try:
            question_status = self.questions_client.submit_question(question=question, commands=commands)
            json_str = json.dumps(question_status, indent=4)
            print("submit:")
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return question_status
        except Exception as e:
            self.handle_exception(e)

    def check_question_status(self, ticket_number: str=""):
        try:
            question_status = self.questions_client.check_question_status(ticket_number)
            json_str = json.dumps(question_status, indent=4)
            print("status:")
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return question_status
        except Exception as e:
            self.handle_exception(e)

    def fetch_answer(self, ticket_number: str="", page: int=1, limit: int=10, is_batch_pages: bool=False, max_page_count: int=10):
        try:
            answer = self.questions_client.fetch_answer(ticket_number, page=page, limit=limit, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            json_str = json.dumps(answer, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return answer
        except Exception as e:
            self.handle_exception(e)


def get_question():
    # Check if an argument was passed
    if len(sys.argv) > 1:
        # The first argument is always the script name, so the second one (index 1) is the parameter you passed
        question = sys.argv[1]
        print(f"Received question: {question}")
    else:
        print("No question was passed.  using a default question of 'Top Sponsors in NSCLC'")
        print("You can pass a question as an argument to this script, e.g. 'python questions.py \"Top Sponsors in NSCLC\"'")
        question = "Top Sponsors in NSCLC"
    return question

def main():
    question = get_question()

    huma_client = HumaSDKQuestionsClient(service_name="Questions")

    commands = []  # write your required commands visit documentation for more details
    submission_status = huma_client.submit_question(question=question, commands=commands)
    ticket_number = submission_status.get('ticket_number')

    #only applicable if response data is paginated
    page, limit = 1, 100
    max_page_count = 100
    is_batch_pages = bool(max_page_count)

    if 'error_message' in submission_status:
        print(f'Failed to submit question {question}, because {submission_status["error_message"]}')
        exit(1)

    while True:
        print(f"Checking Status of '{ticket_number}' ticket number")
        status_response = huma_client.check_question_status(ticket_number=ticket_number)

        question_status = status_response.get('question_status', '')
        if question_status == 'succeeded':
            print(f"Getting Result of Question with '{ticket_number}' ticket number")
            result_response = huma_client.fetch_answer(ticket_number=ticket_number, page=page, limit=limit, is_batch_pages=is_batch_pages, max_page_count=max_page_count)

            sanitized_question = ''.join(e for e in question if e.isalnum() or e.isspace()).replace(' ', '_')

            # Create 'output' directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save the result to a JSON file
            with open(f'output/{sanitized_question}_result.json', 'w') as f:
                json.dump(result_response, f, indent=4)

            print(f"Result saved to output/{sanitized_question}_result.json")
            break
        elif question_status == 'rejected':
            print(f'The question "{question}" failed to process.')
            break
        else:
            print(f'Question "{question}" is being processed, checking status in 5 seconds...')
            time.sleep(5)


if __name__ == "__main__":
    main()
