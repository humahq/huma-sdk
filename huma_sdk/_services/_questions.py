from huma_sdk._resources import _Services
from huma_sdk._services._paginator import _Paginator

class _Questions(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _handle_pagination(self, caller_function, page, limit, is_batch_pages, max_page_count, *args, **kwargs):
        paginator = _Paginator(self, module="favorites", is_answer_data=True)
        if is_batch_pages:
            return paginator.paginate_result(max_page_count, caller_function, limit, *args, **kwargs)
        else:
            kwargs.update({"page": page, "limit": limit})
            return caller_function(*args, **kwargs)

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

    def fetch_answer(self, ticket_number: str=None, page: int=1, limit: int=50, is_batch_pages: bool=False, max_page_count: int=10):
        args = (ticket_number, )
        result = self._handle_pagination(self._fetch_answer, page, limit, is_batch_pages, max_page_count, *args)
        return result