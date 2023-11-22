import json
import os
import time

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
            print(question_status)
            return question_status
        except Exception as e:
            self.handle_exception(e)

    def fetch_answer(self, ticket_number: str="", page: int=1, limit: int=10):
        try:
            answer = self.questions_client.fetch_answer(ticket_number, page=page, limit=limit)
            json_str = json.dumps(answer, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return answer
        except Exception as e:
            self.handle_exception(e)

    def fetch_paginated_answer(self, result_response, ticket_number, max_page_count=10):
        try:
            answer_data: list = result_response.get('answer', {}).get('data', [])
            for page in range(2, min(max_page_count, result_response.get('metadata', {}).get('page_count', 0) + 1)):
                page_limit = result_response.get('metadata', {}).get('per_page')
                print(f'Fetching {page_limit} records of page {page} in 5 seconds...')
                time.sleep(5)
                result_response = self.fetch_answer(page=page, limit=page_limit, ticket_number=ticket_number)
                new_data = result_response.get('answer', {}).get('data', [])
                answer_data.extend(new_data)

            result_response['answer']['data'] = answer_data
            del result_response['metadata']
            return result_response

        except Exception as e:
            self.handle_exception(e)


def main():
    huma_client = HumaSDKQuestionsClient(service_name="Questions")

    # Example usage
    question = "Planned patient enrollment for pediatric Ewing's Sarcoma trials"
    commands = []  # write your required commands visit documentation for more details
    submission_status = huma_client.submit_question(question=question, commands=commands)
    ticket_number = submission_status.get('ticket_number')

    if 'error_message' in submission_status:
        print(f'Failed to submit question, because {submission_status["error_message"]}')
        return

    while True:
        print(f"Checking Status of '{ticket_number}' ticket number")
        status_response = huma_client.check_question_status(ticket_number=ticket_number)

        question_status = status_response.get('question_status', '')
        if question_status == 'succeeded':
            print(f"Getting Result of Question with '{ticket_number}' ticket number")
            result_response = huma_client.fetch_answer(ticket_number=ticket_number)
            if result_response.get('metadata'):
                result_response = huma_client.fetch_paginated_answer(result_response, ticket_number)

            sanitized_question = ''.join(e for e in question if e.isalnum() or e.isspace()).replace(' ', '_')

            if not os.path.exists("output"):
                os.mkdir("output")

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
