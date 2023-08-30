from huma_sdk._resources import _Services


class _Aliases(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_aliases(self, **params):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/aliases"
        return self._make_request(method="GET", url=url, headers=headers, params=params)

    def fetch_aliases(self, page: int=None, limit: int=None, sort_by: int=-1, order_by: str="", search_by: str="", search_for: str=""):
        params = {"page": page, "limit": limit, "sort_by": sort_by, "order_by": order_by, "search_by": search_by, "search_for": search_for}
        aliases = self._fetch_aliases(**params)
        return aliases