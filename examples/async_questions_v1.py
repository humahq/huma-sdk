import os
import json
import huma_sdk
from typing_extensions import override
from huma_sdk._helpers.event_helpers import EventHandler
from concurrent.futures import ThreadPoolExecutor, as_completed

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

GRAPHQL_API_URL = "https://appsync.dev.009.huma.ai/graphql"

RESULTS_PATH = "_cache/"


class EventHandlerCustom(EventHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.collected_updates = ""
        self._thread_id = ""
        self.answer_files_directory = RESULTS_PATH or ""
        if not os.path.exists(self.answer_files_directory):
            os.mkdir(self.answer_files_directory)

    def create_file(self):
        self.answer_file = f"{self.answer_files_directory}{self._thread_id}_answer.json"
        with open(self.answer_file, 'w') as f:
            f.write(json.dumps({"answers": []}))

    def add_data_in_file(self):
        with open(self.answer_file, "r") as f:
            content = f.read()
            current_answers = json.loads(content) if content else {"answers": []}

        # Add new response to the existing answers
        current_answers["answers"].append(self.collected_updates)
        self.collected_updates = ""

        # Write updated answers to answers.json asynchronously
        with open(self.answer_file, "w") as f:
            f.write(json.dumps(current_answers, indent=2))

    ## callback functions V1
    @override
    def on_debug_update_v1(self, message):
        """"""
        # print(f"{YELLOW}{message['content']}{RESET}")

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
        self.add_data_in_file()

        print(f"{CYAN}Result written to answer.json{RESET}")


def submit_questions(question_list):
    questions_client = huma_sdk.session(
        service_name="Questions",
        mode="async",
        api_version='v1',
        graphql_api_url=GRAPHQL_API_URL
    )

    with questions_client.submit_question(
        question=question_list,
        event_handler=EventHandlerCustom()
    ) as stream:
        stream.create_file()
        stream.untill_done()


def main():
    questions_list = {
        "questions": [
            # Each list will become single threads
            [
                # "search active, phase 2 NSCLC",
                "suggest breast cancer and immunotherapy",
                # "suggest literature analysis for breast cancer and her2+",
                "what do you know about breast cancer and immunotherapy"

            ],
            [
                "suggest breast cancer and precision medicine",
                "top sponsors in active, phase 3 NSCLC",
                # "literature analysis for Lazertinib"

            ]
        ]
    }

    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each question list to the ThreadPoolExecutor
        futures = [executor.submit(submit_questions, q_list) for q_list in questions_list['questions']]

        # Ensure all threads are completed
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
