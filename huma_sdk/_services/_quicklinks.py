from huma_sdk._resources import _Services


class _Quicklinks(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_quicklinks(self):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/quicklinks"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_quicklinks(self):
        quicklinks = self._fetch_quicklinks()
        return quicklinks