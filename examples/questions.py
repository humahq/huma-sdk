import huma_sdk
import time
import json
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


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
            print(question_status)
            return question_status
        except Exception as e:
            self.handle_exception(e)

    def check_question_status(self, ticket_number: str=""):
        try:
            question_status = self.questions_client.check_question_status(ticket_number)
            print(question_status)
            return question_status
        except Exception as e:
            self.handle_exception(e)

    def fetch_answer(self, ticket_number: str="", page: int=1, limit: int=10):
        try:
            answer = self.questions_client.fetch_answer(ticket_number, page=page, limit=limit)
            print(answer)
            return answer
        except Exception as e:
            self.handle_exception(e)


def main():
    huma_client = HumaSDKQuestionsClient(service_name="Questions")

    # Example usage
    question = "exclusion criteria analysis for active phase 3 oncology"
    
    commands = []  # write your required commands visit documentation for more details
    submission_status = huma_client.submit_question(question=question, commands=commands)
    ticket_number = submission_status.get('ticket_number')

    while True:
        print(f"Checking Status of '{ticket_number}' ticket number")
        status_response = huma_client.check_question_status(ticket_number=ticket_number)

        question_status = status_response.get('question_status', '')
        if question_status == 'succeeded':
            print(f"Getting Result of Question with '{ticket_number}' ticket number")
            result_response = huma_client.fetch_answer(ticket_number=ticket_number)

            sanitized_question = ''.join(e for e in question if e.isalnum() or e.isspace()).replace(' ', '_')
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
