from huma_sdk._resources import _Services


class _Subscription(_Services):
    def __init__(self, *args, **kwargs):
        kwargs['service_name'] = 'subscribes'
        super().__init__(*args, **kwargs)

    def _fetch_subscription(self, **params):
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

    def fetch_subscription(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str=None, question: str=None):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "question": question}
        subscription = self._fetch_subscription(**params)
        return subscription

    def create_subscription(self, ticket_number: str=None):
        payload = {"ticket_number": ticket_number}
        subscription = self._create_subscription(**payload)
        return subscription

    def fetch_subscription_data(self, subscribed_id: str=None, page: int=1, limit: int=20, type: str=None):
        params = {"page": page, "limit": limit, "type": type}
        subscription = self._fetch_subscription_data(subscribed_id, **params)
        return subscription
    
    def delete_subscription(self, *args,**kwargs):
        subscription = self._delete_subscription(*args,**kwargs)
        return subscription
    
    def fetch_subscription_status(self, *args,**kwargs):
        subscription = self._fetch_subscription_status(*args,**kwargs)
        return subscription
