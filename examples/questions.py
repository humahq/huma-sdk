import huma_sdk
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
        except Exception as e:
            self.handle_exception(e)

    def check_question_status(self, ticket_number: str=""):
        try:
            question_status = self.questions_client.check_question_status(ticket_number)
            print(question_status)
        except Exception as e:
            self.handle_exception(e)

    def fetch_answer(self, ticket_number: str="", page: int=1, limit: int=10):
        try:
            answer = self.questions_client.fetch_answer(ticket_number, page=page, limit=limit)
            print(answer)
        except Exception as e:
            self.handle_exception(e)


def main():
    huma_client = HumaSDKQuestionsClient(service_name="Questions")

    # Example usage
    question = "<write your question here>"
    commands = []  # write your required commands, visit documentation for more details
    huma_client.submit_question(question=question, commands=commands)

    ticket_number = "<write your ticket number>"
    huma_client.check_question_status(ticket_number)
    huma_client.fetch_answer(ticket_number, page=1, limit=10)

if __name__ == "__main__":
    main()
