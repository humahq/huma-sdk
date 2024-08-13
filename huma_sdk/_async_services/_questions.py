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

        command_to_add = ' '.join(command for command in commands)
        return [f"{q} {command_to_add}" for q in question]

    def _submit_question(self, question: str = None, commands: List[str] = [], **kwargs):
        # Construct the full question string
        questions_list = self.get_questions_list(question, commands)

        # Make the asynchronous request via the chat service
        return self.chat_service.ask_question(question=questions_list, **kwargs)

    def submit_question(self, *args, **kwargs):
        return self._submit_question(*args, **kwargs)


if __name__ == "__main__":
    from typing_extensions import override
    import logging, json

    # Constants
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BLACK = "\033[90m"
    RESET = "\033[0m"


    class EventHandlerCustom(EventHandler):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.collected_updates = ""
            self.answer_file = "answer.json"
            with open(self.answer_file, 'w') as f:
                f.write(json.dumps({"answers": []}))

        def add_data_in_file(self):
            with open(self.answer_file, "r") as f:
                content = f.read()
                current_answers = json.loads(content) if content else {"answers": []}

            # Add new response to the existing answers
            current_answers["answers"].append(self.collected_updates)

            # Write updated answers to answers.json asynchronously
            with open(self.answer_file, "w") as f:
                f.write(json.dumps(current_answers, indent=2))

        ## callback functions V1
        @override
        def on_debug_update_v1(self, message):
            """"""
            # print(f"{BLUE}{message['content']}{RESET}")

        @override
        def on_progress_update_v1(self, message):
            """Overriden Callback function"""
            print(f"{YELLOW}{message['content']}{RESET}")

        @override
        def on_follow_up_update_v1(self, message):
            """Overriden Callback function"""
            print(f"{YELLOW}{message['content']}{RESET}")
            self.collected_updates += message['content']

        @override
        def on_visual_update_v1(self, message):
            """Callback Function"""
            print(f"{GREEN}{message['content']}{RESET}")
            self.collected_updates = message['content']

        @override
        def on_stream_update_v1(self, message):
            """Callback Function"""
            print(f"{GREEN}{message['content']}{RESET}")
            self.collected_updates += message['content']

        @override
        def on_message_completion_v1(self, message):
            """Callback function called when the message is complete"""
            result = {"answer": self.collected_updates.strip()}
            with open("result.json", "w") as json_file:
                json.dump(result, json_file, indent=4)

            print(f"{CYAN}Result written to result.json{RESET}")


        ## callback functions V2
        @override
        def on_debug_update_v2(self, delta):
            """"""
            print(f"{BLUE}{delta['delta']}{RESET}")

        @override
        def on_progress_update_v2(self, delta):
            """Overriden Callback function"""
            print(f"{YELLOW}{delta['delta']}{RESET}")

        @override
        def on_visual_update_v2(self, delta):
            """Callback Function"""
            print(f"{GREEN}{delta['delta']}{RESET}")

        @override
        def on_stream_update_v2(self, delta):
            """Callback Function"""
            print(f"{GREEN}{delta['delta']}{RESET}")


    question_client = _AsyncQuestions(service_name="Questions", api_version="v1")
    with question_client.submit_question(
        question="search active, phase 2 NSCLC",
        event_handler=EventHandlerCustom()
    ) as stream:
        stream.untill_done()