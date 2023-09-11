from huma_sdk._resources import _Services


class _Subscribes(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_subscribes(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscribes"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _create_subscribe(self, **payload):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscribes/create"
        return self._make_request(method="POST", url=url, headers=headers, json=payload)

    def _fetch_subscribe_data(self, subscribed_id, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscribes/{subscribed_id}/data"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def _delete_subscribe(self, subscribed_id):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscribes/{subscribed_id}/delete"
        return self._make_request(method="DELETE", url=url, headers=headers)

    def _fetch_subscribed_status(self, question):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/subscribes/{question}/status"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_subscribes(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str=None, question: str=None):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "question": question}
        subscribes = self._fetch_subscribes(**params)
        return subscribes

    def create_subscribe(self, ticket_number: str=None):
        payload = {"ticket_number": ticket_number}
        subscribe = self._create_subscribe(**payload)
        return subscribe

    def fetch_subscribe_data(self, subscribed_id: str=None, page: int=1, limit: int=20, type: str=None):
        params = {"page": page, "limit": limit, "type": type}
        subscribe = self._fetch_subscribe_data(subscribed_id, **params)
        return subscribe
    
    def delete_subscribe(self, *args, **kwargs):
        subscribe = self._delete_subscribe(*args, **kwargs)
        return subscribe
    
    def fetch_subscribed_status(self, *args, **kwargs):
        subscribe = self._fetch_subscribed_status(*args, **kwargs)
        return subscribe