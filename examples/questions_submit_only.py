from questions_list import QUESTIONS_LIST, COMMANDS
from parallelization import submit_questions_thread_manager

if __name__ == "__main__":
    submit_questions_thread_manager(questions=QUESTIONS_LIST, commands=COMMANDS)

# for local testing purposes you can try using this file to submit questions to the platform
# and receive them by running a webhook listener with command:
# uvicorn huma_sdk_app_wrapper:asgi_app --port 5000 --host 0.0.0.0 --reload
# you should setup a route back to your local machine using ngrok or similar tool with command:
# ngrok http 5000
