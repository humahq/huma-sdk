from typing import List
from huma_sdk._async_resources import _AsyncServices

class _AsyncQuestions(_AsyncServices):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _submit_question(self, question: str=None, commands: List[str]=[], **kwargs):
        question = f"{question} {' '.join(command for command in commands)}"
        self._make_async_request(question=question)


    def submit_question(self, *args, **kwargs):
        submission_status = self._submit_question(*args, **kwargs)
        return submission_status


if __name__ == "__main__":
    question_client = _AsyncQuestions(service_name="Questions", api_version="v1")
    question_client.submit_question(question="what is cancer")