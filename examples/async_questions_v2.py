import os
import json
import huma_sdk
from datetime import datetime
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

GRAPHQL_API_URL = "https://appsync-v2.dev.009.huma.ai/graphql"

RESULTS_ROOT_DIR = "_cache/runs"


class CustomEventHandler(EventHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.collected_updates = ""
        self.error = ""
        self._thread_id = ""

    def create_file(self, answers_location):
        self.answer_file = f"{answers_location}/{self._thread_id}_messages.json"
        with open(self.answer_file, 'w') as f:
            f.write(json.dumps({"output": []}))

    def add_data_in_file(self, result):
        with open(self.answer_file, "r") as f:
            content = f.read()
            current_answers = json.loads(content) if content else {"output": []}

        # Add new response to the existing answers
        actual_result = {
            "question": result.get('question'),
            "answer": self.collected_updates,
            "error": self.error
        }
        current_answers["output"].append(actual_result)
        self.collected_updates, self.error = "", ""

        # Write updated answers to answers.json asynchronously
        with open(self.answer_file, "w") as f:
            f.write(json.dumps(current_answers, indent=2))

    @override
    def on_debug_update(self, delta):
        """Callback function"""
        # print(f"{BLUE}{delta['delta']}{RESET}")

    @override
    def on_progress_update(self, delta):
        """Callback function"""
        print(f"{YELLOW}{delta['delta']}{RESET}")

    @override
    def on_follow_up_update(self, delta):
        """Callback function"""
        print(f"{YELLOW}{delta['delta']}{RESET}")
        self.collected_updates += delta['delta']

    @override
    def on_visual_update(self, delta):
        """Callback function"""
        print(f"{GREEN}{delta['delta']}{RESET}")
        self.collected_updates = delta['delta']

    @override
    def on_stream_update(self, delta):
        """Callback function"""
        print(f"{GREEN}{delta['delta']}{RESET}")
        self.collected_updates += delta['delta']

    @override
    def on_new_question_asked(self, question):
        """Callback function"""
        print(f"Asked New Question: {MAGENTA}{question}{RESET}")

    @override
    def on_error_update(self, delta):
        """Callback function"""
        print(f"{RED}{delta['delta']}{RESET}")
        self.error = delta['delta']


    @override
    def on_message_completion(self, message, result):
        """Callback function"""
        self.add_data_in_file(result)
        print(f"{CYAN}Result written to {self.answer_file}{RESET}")


def create_results_directory():
    os.makedirs(RESULTS_ROOT_DIR, exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    subdirectory_path = os.path.join(RESULTS_ROOT_DIR, current_time)
    os.makedirs(subdirectory_path, exist_ok=True)

    return subdirectory_path


def submit_questions(question_set, answers_location):
    questions_client = huma_sdk.session(
        service_name="Questions",
        mode="async",
        api_version='v2',
        graphql_api_url=GRAPHQL_API_URL
    )

    with questions_client.submit_question(
        question=question_set['questions_details'],
        topic=question_set['description'],
        agent=question_set['agent'],
        event_handler=CustomEventHandler()
    ) as stream:
        stream.create_file(answers_location)
        stream.until_done()


def main():
    questions_list = [
        # Each dict will become single threads
        {
            "agent": "Research",
            "description": "Nsclc Questions",
            "questions_details": [
                {
                    "question": "suggest breast cancer and immunotherapy",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "suggest literature analysis for breast cancer and her2+",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "what do you know about breast cancer and immunotherapy",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "search active, phase 2 NSCLC",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                }
            ]
        },
        {
            "agent": "Research",
            "description": "Nsclc Questions 2",
            "questions_details": [
                {
                    "question":"suggest breast and precision medicine",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "top sponsors in active, phase 3 NSCLC",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "suggest literature analysis for breast cancer and her2+",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                },
                {
                    "question": "what do you know about breast cancer and immunotherapy",
                    "focus": "research",
                    "sources": ["pubmed", "pubmed_central"]
                }
            ]
        }
    ]

    answers_location = create_results_directory()
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit each question list to the ThreadPoolExecutor
        futures = [executor.submit(submit_questions, q_list, answers_location) for q_list in questions_list]

        # Ensure all threads are completed
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()