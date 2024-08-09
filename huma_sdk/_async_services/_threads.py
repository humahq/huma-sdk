from typing import List
from huma_sdk._async_resources import _AsyncServices

class _Threads(_AsyncServices):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _create(self, topic: str=None, **kwargs):
        self._make_async_request(topic=topic, *kwargs)


    def create(self, *args, **kwargs):
        submission_status = self._create(*args, **kwargs)
        return submission_status