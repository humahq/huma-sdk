from huma_sdk._resources import _Services


class _Audits(_Services):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _fetch_audits(self):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/audits"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_audits(self):
        audits = self._fetch_audits()
        return audits