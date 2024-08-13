from typing import List
from huma_sdk._async_resources import ChatServiceV1, ChatServiceV2

class _Threads:
    def __init__(self, service_name=None, api_version="v1", **kwargs):
        # Initialize the appropriate chat service based on the API version
        if api_version == "v1":
            self.chat_service = ChatServiceV1(service_name=service_name, **kwargs)
        elif api_version == "v2":
            self.chat_service = ChatServiceV2(service_name=service_name, **kwargs)
        else:
            raise ValueError(f"Unsupported API version: {api_version}")


    def _create(self, topic: str=None, **kwargs):
        self.chat_service.start_new_chat(topic=topic, *kwargs)


    def create(self, *args, **kwargs):
        submission_status = self._create(*args, **kwargs)
        return submission_status