import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError
import concurrent.futures
from typing import List
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import json

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
            print(highlight(json.dumps(answer, indent=4, sort_keys=True), JsonLexer(), TerminalFormatter()))
            print(answer)
            return answer
        except Exception as e:
            self.handle_exception(e)

def submit_questions(questions: List, commands: List=[]):
    huma_client = HumaSDKQuestionsClient(service_name="Questions")
    for question in questions:
        huma_client.submit_question(question=question, commands=commands)
    pass

def submit_questions_thread_manager(questions: List[str], commands: List=[]):
    list_of_batches_of_questions = _get_question_batches(questions, batch_size=15)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(submit_questions, batch, commands) for batch in list_of_batches_of_questions]
        batches_of_questions = [f.result() for f in futures]

    return None

def _get_question_batches(questions: List[dict], batch_size: int = 1) -> List[List[str]]:
    '''
    get batch definitions of questions
    --------
        Args:
            A list of Huma Platform v2 Questions as strings

        Returns:
            batch_size is the maximum items per batch
    '''
    batches_of_questions = []
    # Start a loop over the iterable
    for index in range(0, len(questions), batch_size):
        # Create a new iterable by slicing the original
        batches_of_questions.append(questions[index: min(index + batch_size, len(questions))])
    return batches_of_questions
