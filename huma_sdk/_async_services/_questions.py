from typing import List
from huma_sdk._helpers.event_helpers import EventHandler
from huma_sdk._async_resources import ChatServiceV1, ChatServiceV2

class _AsyncQuestions:
    def __init__(self, service_name=None, api_version="v1", **kwargs):
        # Initialize the appropriate chat service based on the API version
        if api_version == "v1":
            self.chat_service = ChatServiceV1(service_name=service_name, **kwargs)
        elif api_version == "v2":
            self.chat_service = ChatServiceV2(service_name=service_name, **kwargs)
        else:
            raise ValueError(f"Unsupported API version: {api_version}")

    def get_questions_list(self, question, commands):
        if isinstance(question, str):
            question = [question]

        command_to_add = ''.join(f" {command}" for command in commands)
        return [f"{q}{command_to_add}" for q in question]

    def _submit_question(self, question: str = None, commands: List[str] = [], **kwargs):
        # Construct the full question string
        questions_list = self.get_questions_list(question, commands)

        # Make the asynchronous request via the chat service
        return self.chat_service.ask_question(question=questions_list, **kwargs)

    def submit_question(self, *args, **kwargs):
        return self._submit_question(*args, **kwargs)