from types import TracebackType
from huma_sdk._utils import parse_json_response


class EventHandler:
    def __init__(self) -> None:
        self._result = {}

    def _init(self, stream, result, thread_id, questions_queue, send_message_function):
        self._stream = stream
        self._result = result
        self._thread_id = thread_id
        self._questions_queue = questions_queue
        self._total_questions = self._questions_queue.size()
        self._executed_questions = 0
        self._executed_messages = []
        self._send_message_function = send_message_function

    def update_result(self, key, value):
        if key in self._result and self._result.get(key):
            self._result[key].update(value)
        else:
            self._result[key] = value

    ## V1 Callback Functions
    def on_visual_update_v1(self, message):
        """Callback Function"""

    def on_stream_update_v1(self, message):
        """Callback Function"""

    def on_debug_update_v1(self, message):
        """Callback Function"""

    def on_progress_update_v1(self, message):
        """Callback function"""

    def on_follow_up_update_v1(self, message):
        """Callback Function"""

    def on_message_completion_v1(self, message, full_result):
        """"""

    def on_error_update_v1(self, message):
        """"""

    def on_new_question_asked_v1(self, question):
        """"""

    ## V2 Callback Functions
    def on_visual_update_v2(self, delta):
        """Callback Function"""

    def on_stream_update_v2(self, delta):
        """Callback Function"""

    def on_debug_update_v2(self, delta):
        """Callback Function"""

    def on_progress_update_v2(self, delta):
        """Callback function"""

    def check_final_processing(self):
        return all([value.get('final_status') for value in list(self._result.values())])

    def submit_question(self, question):
        message_id = self._send_message_function(question)
        result = { "question": question, "final_status": False, "submission_status": True }
        self.on_new_question_asked_v1(question)
        self.update_result(message_id, value=result)

    def submit_question_from_queue(self):
        if not self._executed_questions and not self._result:
            question = self._questions_queue.pop()
            if question:
                self.submit_question(question)

        elif self.check_final_processing():
            question = self._questions_queue.pop()
            if question:
                self.submit_question(question)


    def until_done(self):
        while self._stream:
            self.submit_question_from_queue()
            ...

    def check_closing_condition(self, message):
        is_message_completed = False
        if message.get("contentType") == "system" and message.get("contentsubType") in ["system", "blocking"]:
            message_content_json = parse_json_response(message.get("content"))
            is_chat_processed = message_content_json.get("is_processed")

            if is_chat_processed and message['messageId'] not in self._executed_messages:
                self._executed_messages.append(message['messageId'])
                self._executed_questions += 1
                is_message_completed = True

        return is_message_completed

    def check_closing_condition_v2(self, message):
        is_chat_processed = False
        if message["author"]['role'] == "system_manager":
            is_chat_processed = message['event_metadata']['event_data']['message_metadata']['processing_status']['state'] in ["done", "failure"]

        return is_chat_processed

    def handle_final_operations(self, message):
        is_message_completed = self.check_closing_condition(message)
        if is_message_completed:
            value = { "final_status": True, "submission_status": True }
            self.update_result(key=message['messageId'], value=value)

            self.on_message_completion_v1(message, self._result.get(message['messageId']))
            is_chat_processed = self._executed_questions == self._total_questions
            if is_chat_processed:
                self._stream = False

            return is_chat_processed

    def _emit_subscription_event(self, message):
        if message['contentType'] == "stream":
            self.on_stream_update_v1(message)

        elif message['contentsubType'] == "status":
            self.on_progress_update_v1(message)

        elif message['contentsubType'] == "debug":
            self.on_debug_update_v1(message)

        elif message['contentType'] == "analyzer" and message['debug_and_status_state'] == "complete":
            self.on_visual_update_v1(message)

        elif message['contentType'] == "follow_up" and message['debug_and_status_state'] == "complete":
            self.on_follow_up_update_v1(message)

        elif message['contentType'] == "error":
            message['content'] = parse_json_response(message['content'])
            self.on_error_update_v1(message)

        is_chat_processed = self.handle_final_operations(message)
        return is_chat_processed

    def _emit_subscription_event_v2(self, message):

        if message['author']['role'] == "streaming_assistant":
            self.on_stream_update_v2(message['event_metadata']['event_data']['sub_message_metadata']['delta'])

        elif message['author']['role'] == "progress_assistant":
            delta = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            if delta['delta_type'] in ["status", "step_status"]:
                self.on_progress_update_v2(delta)
            elif delta['delta_type'] == "log_info":
                self.on_debug_update_v2(delta)

        elif message['author']['role'] == "visual_assistant":
            visual = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            self.on_visual_update_v2(visual)

        is_chat_processed = self.check_closing_condition_v2(message)
        return is_chat_processed


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
        self.__stream = False