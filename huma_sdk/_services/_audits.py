from huma_sdk._resources import _Services


class _Audits(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_audits(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/audits"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def fetch_audits(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str="created", endpoint: str="", content: str=""):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "endpoint": endpoint, "content": content}
        audits = self._fetch_audits(**params)
        return audits