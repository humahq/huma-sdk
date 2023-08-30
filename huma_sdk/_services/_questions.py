from huma_sdk._resources import _Services


class _Questions(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _submit_question(self, **payload):
        headers = {"Authorization": f"Bearer {self.api_secret_key}", "Content-Type": "application/json"}
        url = f"{self.api_url}/v1/questions"
        return self._make_request(method="POST", url=url, headers=headers, json=payload)

    def _check_question_status(self, ticket_number):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/questions/{ticket_number}/status"
        return self._make_request(method="GET", url=url, headers=headers)

    def _fetch_answer(self, ticket_number, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/questions/{ticket_number}/result"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def submit_question(self, question: str="", commands: list=None, answer_format: str="json"):
        payload = {"question": question, "commands": commands or [], "answer_format": answer_format}
        submission_status = self._submit_question(**payload)
        return submission_status

    def check_question_status(self, *args, **kwargs):
        question_status = self._check_question_status(*args, **kwargs)
        return question_status

    def fetch_answer(self, ticket_number: str=None, page: int=1, limit: int=50):
        params = {'page': page, "limit": limit}
        submission_status = self._fetch_answer(ticket_number, **params)
        return submission_status