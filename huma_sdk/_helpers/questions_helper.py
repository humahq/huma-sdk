from collections import deque

class QuestionQueue:
    def __init__(self):
        # Initialize a deque to maintain the queue of questions
        self.queue = deque()

    def push(self, question: str):
        """
        Add a question to the end of the queue.

        :param question: The question to be added.
        """
        self.queue.append(question)

    def pop(self) -> str:
        """
        Remove and return the question at the front of the queue.

        :return: The question at the front of the queue.
        """
        if self.is_empty():
            return None

        return self.queue.popleft()

    def peek(self) -> str:
        """
        Return the question at the front of the queue without removing it.

        :return: The question at the front of the queue.
        """
        if self.is_empty():
            return None

        return self.queue[0]

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.

        :return: True if the queue is empty, False otherwise.
        """
        return len(self.queue) == 0

    def size(self) -> int:
        """
        Return the number of questions in the queue.

        :return: The size of the queue.
        """
        return len(self.queue)

    def clear(self):
        """
        Clear all questions from the queue.
        """
        self.queue.clear()
        print("The queue has been cleared.")
