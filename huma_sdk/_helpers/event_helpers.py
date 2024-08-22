from types import TracebackType
from huma_sdk._utils import parse_json_response
from typing import Callable, Any, Dict, Optional
from huma_sdk._helpers.questions_helper import QuestionQueue


class EventHandler:
    def __init__(self) -> None:
        self._result = {}
        self._stream: bool = True
        self._result: Dict[str, Any] = {}
        self._thread_id: Optional[str] = None
        self._questions_queue: Optional[QuestionQueue] = None
        self._send_message_function: Optional[Callable[[str], str]] = None
        self._total_questions: int = 0
        self._executed_questions: int = 0
        self._executed_messages: list = []

    def _init(self, stream, result, thread_id, questions_queue, send_message_function):
        self._stream = stream
        self._result = result
        self._thread_id = thread_id
        self._questions_queue = questions_queue
        self._total_questions = self._questions_queue.size()
        self._executed_questions = 0
        self._executed_messages = []
        self._send_message_function = send_message_function

    @property
    def remaining_questions(self):
        return bool(self._total_questions-self._executed_questions)

    @property
    def queue_size(self):
        return self._questions_queue.size()

    @property
    def should_submit_question(self):
        return self.queue_size == self._total_questions or self.check_final_processing()

    def update_result(self, key: str, value: Any) -> None:
        if key in self._result and self._result.get(key):
            self._result[key].update(value)
        else:
            self._result[key] = value

    def update_final_result(self, message_id):
        value = { "final_status": True, "submission_status": True }
        self.update_result(key=message_id, value=value)

    def check_final_processing(self):
        return all([value.get('final_status') for value in list(self._result.values())])

    def submit_question(self, question, **kwargs):
        if isinstance(question, dict):
            kwargs = dict(
                focus=question.get('focus'),
                sources=question.get('sources')
            )
            question = question.get('question')

        message_id = self._send_message_function(question, **kwargs)
        result = { "question": question, "final_status": False, "submission_status": True }
        self.on_new_question_asked(question)
        self.update_result(message_id, value=result)

    def submit_question_from_queue(self):
        if self.should_submit_question:
            question = self._questions_queue.pop()
            self.submit_question(question)

    def on_visual_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for visual updates."""

    def on_stream_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for stream updates."""

    def on_debug_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for debug updates."""

    def on_progress_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for progress updates."""

    def on_follow_up_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for follow-up updates."""

    def on_message_completion(self, message: Dict[str, Any], full_result: Any) -> None:
        """Callback Function when a message is completed."""

    def on_error_update(self, message: Dict[str, Any]) -> None:
        """Callback Function for error updates."""

    def on_new_question_asked(self, question: str) -> None:
        """Callback Function when a new question is asked."""

    def check_closing_condition_v1(self, message):
        is_message_completed = False
        if message.get("contentType") == "system" and message.get("contentsubType") in ["system", "blocking"]:
            message_content_json = parse_json_response(message.get("content"))
            is_chat_processed = message_content_json.get("is_processed")

            if is_chat_processed and message['messageId'] not in self._executed_messages:
                self._executed_messages.append(message['messageId'])
                self._executed_questions += 1
                is_message_completed = True

        return is_message_completed

    def handle_final_operations_v1(self, message):
        is_message_completed = self.check_closing_condition_v1(message)
        if is_message_completed:
            self.update_final_result(message_id=message['messageId'])
            self.on_message_completion(message, self._result.get(message['messageId']))

    def handle_final_operations_v2(self, message):
        if message["event_type"] in ["thread_message_done", "thread_message_failure"]:
            self._executed_questions += 1
            message_id = message['event_metadata']['event_data']['id']
            self.update_final_result(message_id=message_id)
            self.on_message_completion(message, self._result.get(message_id))

    def handle_v1_event(self, message):
        if message['contentType'] == "stream":
            self.on_stream_update(message)

        elif message['contentsubType'] == "status":
            self.on_progress_update(message)

        elif message['contentsubType'] == "debug":
            self.on_debug_update(message)

        elif message['contentType'] == "analyzer" and message['debug_and_status_state'] == "complete":
            self.on_visual_update(message)

        elif message['contentType'] == "follow_up" and message['debug_and_status_state'] == "complete":
            self.on_follow_up_update(message)

        elif message['contentType'] == "error":
            message['content'] = parse_json_response(message['content'])
            self.on_error_update(message)

    def handle_v2_event(self, message):
        if message['author']['role'] == "streaming_assistant":
            delta = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            if delta['delta_type'] == "replace":
                self.on_follow_up_update(delta)
            elif delta['delta_type'] == "add":
                self.on_stream_update(delta)

        elif message['author']['role'] == "progress_assistant":
            delta = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            if delta['delta_type'] == "step_status":
                actual_delta = parse_json_response(delta['delta'])
                delta['delta'] = actual_delta.get('title') if isinstance(actual_delta, dict) else actual_delta
                self.on_progress_update(delta)
            elif delta['delta_type'] == "status":
                self.on_progress_update(delta)
            elif delta['delta_type'] in ["log_info", "log_error", "log_warning", "log_debug"]:
                self.on_debug_update(delta)

        elif message['author']['role'] == "visual_assistant":
            visual = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            self.on_visual_update(visual)

        elif message['event_type'] == "thread_message_failure":
            delta = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            self.on_error_update(delta)

    def _emit_subscription_event(self, message, api_version):
        if api_version == "v1":
            self.handle_v1_event(message)
            self.handle_final_operations_v1(message)

        elif api_version == "v2":
            message_id = message['event_metadata']['event_data']['id']
            if message_id in self._result.keys():
                self.handle_v2_event(message)
                self.handle_final_operations_v2(message)

        if not self.remaining_questions:
            self._stream = False

        return not self.remaining_questions

    def until_done(self):
        while self._stream:
            if self.queue_size:
                self.submit_question_from_queue()


class ThreadEventManager:
    def __init__(self, event_handler, result, thread_id, questions_queue, send_message_function) -> None:
        self.__stream:bool = True
        self.__result = result
        self.__thread_id = thread_id
        self.__questions_queue=questions_queue
        self.__send_message_function=send_message_function
        self.__event_handler = event_handler or EventHandler()

    def __enter__(self):
        self.__event_handler._init(
            self.__stream,
            self.__result,
            self.__thread_id,
            self.__questions_queue,
            self.__send_message_function
        )
        return self.__event_handler

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        self.__event_handler._stream = False