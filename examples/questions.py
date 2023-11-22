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

    def fetch_answer_data(self, ticket_number, max_page_count=10, limit: int=25):
        try:
            result_response = self.fetch_answer(ticket_number=ticket_number, limit=limit)

            if 'metadata' in result_response:
                #validating max_page_count
                if not isinstance(max_page_count, int):
                    max_page_count = 3

                answer_data: list = result_response.get('answer', {}).get('data', [])
                total_records_present = result_response['metadata'].get('total_count', 0)
                print(f"Total records present: {total_records_present}")
                pages_to_fetch = min(max_page_count, result_response['metadata'].get('page_count', 0))
                total_records = min(pages_to_fetch * int(limit), result_response['metadata'].get('total_count', 0))
                if total_records < total_records_present:
                    print(f"Restricting total records to {total_records} only because max_page_count is set to {max_page_count} with per page limit as {limit}.")


                print(f"Successfully fetched {limit} records out of {total_records}. Fetching records for page 2.")
                print("Next fetch in 5 seconds...")
                time.sleep(5)

                # Fetch additional pages
                for page in range(2, pages_to_fetch + 1):
                    page_limit = result_response['metadata'].get('per_page')
                    result_response = self.fetch_answer(page=page, limit=page_limit, ticket_number=ticket_number)
                    new_data = result_response.get('answer', {}).get('data', [])
                    answer_data.extend(new_data)

                    if page != pages_to_fetch:
                        print(f"Successfully fetched {(page) * page_limit} records out of {total_records}. Fetching records for page {page + 1}.")
                        print("Next fetch in 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"Successfully fetched {(page) * page_limit} records out of {total_records}.")

                # Update the response structure
                result_response['answer']['data'] = answer_data
                del result_response['metadata']

            return result_response

        except Exception as e:
            self.handle_exception(e)


def main():
    huma_client = HumaSDKQuestionsClient(service_name="Questions")

    # Example usage
    question = "Top Sponsors in NSCLC"
    commands = []  # write your required commands visit documentation for more details
    submission_status = huma_client.submit_question(question=question, commands=commands)
    ticket_number = submission_status.get('ticket_number')

    #only applicable if answer data is paginated
    max_page_count = 10
    limit = 100

    if 'error_message' in submission_status:
        print(f'Failed to submit question, because {submission_status["error_message"]}')
        return

    while True:
        print(f"Checking Status of '{ticket_number}' ticket number")
        status_response = huma_client.check_question_status(ticket_number=ticket_number)

        question_status = status_response.get('question_status', '')
        if question_status == 'succeeded':
            print(f"Getting Result of Question with '{ticket_number}' ticket number")
            result_response = huma_client.fetch_answer_data(ticket_number, max_page_count=max_page_count, limit=limit)

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
