from huma_sdk._resources import _Services
from huma_sdk._services._paginator import _Paginator

class _Subscriptions(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _validate_page_number(self, page):
        return page or 1

    def _handle_pagination(self, caller_function, page, limit, is_batch_pages, max_page_count, is_answer_data:bool= True, *args, **kwargs):
        page = self._validate_page_number(page)
        paginator = _Paginator(self, module="subscriptions", is_answer_data=is_answer_data)
        if is_batch_pages:
            return paginator.paginate_result(max_page_count, caller_function, page, limit, *args, **kwargs)
        else:
            kwargs.update({"page": page, "limit": limit})
            return caller_function(*args, **kwargs)

    def _fetch_subscriptions(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscription"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _create_subscription(self, **payload):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscription/create"
        return self._make_request(method="POST", url=url, headers=headers, json=payload)

    def _fetch_subscription_data(self, subscribed_id, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscription/{subscribed_id}/data"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _delete_subscription(self, subscribed_id):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscription/{subscribed_id}/delete"
        return self._make_request(method="DELETE", url=url, headers=headers)

    def _fetch_subscription_status(self, question):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscription/{question}/status"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_subscriptions(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str=None, question: str=None, is_batch_pages: bool=False, max_page_count: int=10):
        params = {"sort_by": sort_by, "order_by": order_by, "question": question}
        subscription = self._handle_pagination(self._fetch_subscriptions, page, limit, is_batch_pages, max_page_count, False, **params)
        return subscription

    def create_subscription(self, ticket_number: str=None):
        payload = {"ticket_number": ticket_number}
        subscription = self._create_subscription(**payload)
        return subscription

    def fetch_subscription_data(self, subscribed_id: str=None, page: int=1, limit: int=20, type: str=None, is_batch_pages: bool = False, max_page_count: int = 10):
        args, params = (subscribed_id, ), {"type": type}
        subscription = self._handle_pagination(self._fetch_subscription_data, page, limit, is_batch_pages, max_page_count, True, *args, **params)
        return subscription

    def delete_subscription(self, *args,**kwargs):
        subscription = self._delete_subscription(*args,**kwargs)
        return subscription

    def fetch_subscription_status(self, *args,**kwargs):
        subscription = self._fetch_subscription_status(*args,**kwargs)
        return subscription