from huma_sdk._resources import _Services


class _Aliases(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_aliases(self):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/aliases"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_aliases(self):
        aliases = self._fetch_aliases()
        return aliases

    