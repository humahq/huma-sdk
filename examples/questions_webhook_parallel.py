from questions_list import QUESTIONS_LIST, COMMANDS
from parallelization import submit_questions_thread_manager

if __name__ == "__main__":
    submit_questions_thread_manager(questions=QUESTIONS_LIST, commands=COMMANDS)
