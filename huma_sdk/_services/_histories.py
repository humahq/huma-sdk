from huma_sdk._resources import _Services


class _Histories(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _fetch_history(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/histories"
        return self._make_request(method="GET", url=url, headers=headers, params=params)
    
    def _fetch_history_data(self, ticket_number, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/histories/{ticket_number}/data"
        return self._make_request(method="GET", url=url, headers=headers, params=params)
    
    def _submit_history_visual(self, **payload):
        headers = {"Authorization": f"Bearer {self.api_secret_key}", "Content-Type": "application/json"}
        url = f"{self.api_url}/v1/histories/visual"
        return self._make_request(method="POST", url=url, headers=headers, json=payload)

    def _check_history_visual_status(self, conversion_id):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/histories/{conversion_id}/visual/status"
        return self._make_request(method="GET", url=url, headers=headers)

    def _fetch_history_visual_result(self, conversion_id):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/histories/{conversion_id}/visual/result"
        return self._make_request(method="GET", url=url, headers=headers)
    
    def fetch_history(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str="", question: str=""):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "question": question}
        history = self._fetch_history(**params)
        return history
    
    def fetch_history_data(self, ticket_number: str=None, page: int=1, limit: int=20, type: str=None):
        params = {"page": page, "limit": limit, "type": type}
        submission_status = self._fetch_history_data(ticket_number, **params)
        return submission_status

    def submit_history_visual(self, ticket_number: str="", file_type: str="", visual_type: str=""):
        payload = {"ticket_number": ticket_number, "file_type": file_type, "visual_type": visual_type}
        submission_status = self._submit_history_visual(**payload)
        return submission_status

    def check_history_visual_status(self, *args):
        question_status = self._check_history_visual_status(*args)
        return question_status

    def fetch_history_visual_result(self, *args):
        submission_status = self._fetch_history_visual_result(*args)
        return submission_status