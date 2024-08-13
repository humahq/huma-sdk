import requests, threading, json
from typing_extensions import override
from huma_sdk._utils import parse_json_response
from huma_sdk._schema.inputs import SendMessageInput
from huma_sdk._helpers.questions_helper import QuestionQueue
from huma_sdk._helpers.event_helpers import ThreadEventManager
from huma_sdk._helpers.async_helpers import SubscriptionClient, AppsyncSchemaClient

# Constants
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class BaseChatService(SubscriptionClient, AppsyncSchemaClient):
    def __init__(self, service_name=None, api_version="v1", **kwargs):
        self.service_name = service_name
        self.api_version = api_version
        self.chat_id = None
        self.message_id = None
        self.should_stop = False  # Variable to control the loop
        self.final_messages = None  # Variable to store final messages
        self.questions_queue = QuestionQueue()
        super().__init__(**kwargs)

    def get_headers(self):
        return {'authorization': f"Bearer {self.api_secret_key}"}

    def error(self, error):
        raise Exception(error)

    def execute_gql(self, query, variables=None):
        data = {
            'query': query,
            'variables': variables,
        }
        response = requests.post(self.graphql_api_url, headers=self.get_headers(), json=data)
        return response.json()

    def handle_subscription(self, subscription_query, variables, callback, connection_name):
        threading.Thread(target=self.subscription_thread, args=(subscription_query, variables, callback, connection_name)).start()

    def event_manager(self, data):
        """Callback Function"""

    def subscribe_to_messages(self, variables=None, connection_name=None):
        subscription_schema = self.get_schema(type="UpdateMessageSubscription", version=self.api_version)
        self.handle_subscription(
            subscription_schema, variables,
            self.event_manager, connection_name=connection_name
        )

    def fetch_answer_data(self, variables=None):
        query = self.get_schema(type="GetAnswerData", version=self.api_version)
        response = self.execute_gql(query, variables)
        return response['data']['getAnswerData']



class ChatServiceV1(BaseChatService):
    def __init__(self, service_name=None, **kwargs):
        super().__init__(service_name, api_version="v1", **kwargs)

    def get_utterance_id_variables(self, message_content, page, limit):
        utterance_id = parse_json_response(message_content).get('utterance_id')
        return {'utteranceId': utterance_id, "page": page, "limit": limit}

    def manage_visual_response(self, message):
        page, limit, has_next_page, result = 1, 100, True, []
        self.logger.info(f'Received Answer Id, Fetching answer data in batches of {limit} records')
        while has_next_page:
            self.logger.info(f'Fetching answer data for batch {page}')
            variables = self.get_utterance_id_variables(message['content'], page, limit)
            response = self.fetch_answer_data(variables)
            has_next_page = response.get('hasNextPage')
            page+=1
            limit+=100
            result.extend(parse_json_response(response.get('data')))

        message['content'] = result
        return message

    @override
    def event_manager(self, message):
        if message.get('contentType') == "analyzer" and message.get('debug_and_status_state') == "complete":
            message = self.manage_visual_response(message)

        return self.event_handler._emit_subscription_event(message)

    def get_messages(self, thread_id, **kwargs):
        query = self.get_schema(type="GetMessages", api_version=self.api_version)
        variables = {
            "chatId": thread_id,
            "page": kwargs.get('page', 1),
            "limit": kwargs.get('limit', 5),
            "type": kwargs.get('type', 'status'),
        }
        response = self.execute_gql(query, variables)
        return response['data']['GetMessages']

    def start_new_chat(self, topic=None, agent=None):
        query = self.get_schema(type="NewChat", version=self.api_version, topic=topic)
        variables = None
        response = self.execute_gql(query, variables=variables)
        self.chat_id = response['data']['newChat']['id']

    def send_message(self, message_content):
        query = self.get_schema(type="SendMessage", version=self.api_version)
        message_input = {
            "respondingToMessageId": "",
            "contentType": "question",
            "content": message_content,
            "isNewChat": True
        }
        variables = {"chatId": self.chat_id, "message": message_input, "source": "bot"}
        response = self.execute_gql(query, variables)
        self.message_id = response['data']['sendMessage']['messageId']
        self.process_utterance(message_content)
        return self.message_id

    def process_utterance(self, message_content):
        query = self.get_schema(type="ProcessUtterance", version=self.api_version)
        variables = {"chatId": self.chat_id, "respondingToMessageId": self.message_id, "utterance": message_content}
        response = self.execute_gql(query, variables)
        return response

    def ask_question(self, question: list, thread_id: str=None, topic: str = None, event_handler=None):
        if not thread_id:
            topic = topic or (question[0] if isinstance(question, list) else question)
            self.start_new_chat(topic=topic)
        else:
            response = self.get_messages(thread_id)
            if not response:
                raise Exception("Wrong thread Id")
            else:
                self.chat_id = thread_id

        variables = {'chatId': self.chat_id}
        self.event_handler = event_handler
        self.subscribe_to_messages(variables=variables, connection_name="subscribeUpdateMessage")

        result = {}
        for q in question:
            self.questions_queue.push(q)

        return ThreadEventManager(
            event_handler=event_handler,
            result=result, thread_id=self.chat_id,
            questions_queue=self.questions_queue,
            send_message_function=self.send_message
        )


class ChatServiceV2(BaseChatService):
    def __init__(self, service_name=None, **kwargs):
        super().__init__(service_name, api_version="v2", **kwargs)

    def get_utterance_id_variables(self, message_content, page, limit):
        utterance_id = parse_json_response(message_content).get('utterance_id')
        return {'utterance_id': utterance_id, "page": page, "limit": limit }

    def manage_visual_response(self, message):
        page, limit, has_next_page, result = 1, 100, True, []
        self.logger.info(f'Received Answer Id, Fetching answer data in batches of {limit} records')
        while has_next_page:
            self.logger.info(f'Fetching answer data for batch {page}')
            visual = message['event_metadata']['event_data']['sub_message_metadata']['delta']
            variables = self.get_utterance_id_variables(visual['delta'], page, limit)
            response = self.fetch_answer_data(variables)
            has_next_page = response.get('hasNextPage')
            page+=1
            limit+=100
            result.append(parse_json_response(response.get('data')))

        message['event_metadata']['event_data']['sub_message_metadata']['delta']['delta'] = result
        return message

    @override
    def event_manager(self, message):
        if message['author']['role'] == "visual_assistant":
            self.manage_visual_response(message)

        return self.event_handler._emit_subscription_event_v2(message)

    def set_user_details(self, response):
        author_metadata = response['data']['newChat']['author']['metadata']
        self.user_details = json.loads(author_metadata).get('user_detals')

    def get_variables(self, **kwargs):
        return SendMessageInput(**{
            "chat_id": self.chat_id,
            "focus": kwargs.get('focus', ""),
            "sources": kwargs.get('sources', []),
            "message_intent": kwargs.get('message_intent', 'question'),
            "user_message": {
                "content": {
                    "type": kwargs.get('type', "text"),
                    "message": kwargs.get('question')
                },
                "author": { "role": kwargs.get('role', "user") }
            }
        }).model_dump()

    def send_message_variables(self, **kwargs):
        return {
            "chat_id": kwargs.get('chat_id'),
            "focus": kwargs.get('focus'),
            "sources": kwargs.get('sources')
        }

    def get_messages(self, thread_id, **kwargs):
        query = self.get_schema(type="GetMessages", version=self.api_version)
        variables = {
            "chat_id": thread_id,
            "page": kwargs.get('page', 1),
            "limit": kwargs.get('limit', 5),
            "offset": kwargs.get('offset', 0)
        }
        response = self.execute_gql(query, variables=variables)
        return response['data']['GetMessages']

    def start_new_chat(self, topic=None, agent="home"):
        query = self.get_schema(type="NewChat", version=self.api_version, topic=topic)
        variables = {
            "topic": topic,
            "agent": agent
        }
        response = self.execute_gql(query, variables=variables)
        self.set_user_details(response)
        self.chat_id = response['data']['newChat']['id']

    def send_message(self, **kwargs):
        query = self.get_schema(type="SendMessage", version=self.api_version)
        variables = self.get_variables(**kwargs)
        self.execute_gql(query, variables)

    def ask_question(self, question: str, thread_id: str=None, topic: str = None, event_handler=None):
        if not thread_id:
            self.start_new_chat(topic=topic or question)
        else:
            response = self.get_messages(thread_id)
            if not response:
                raise Exception("Wrong thread Id")
            else:
                self.chat_id = thread_id

        self.send_message(question=question)
        self.event_handler = event_handler
        self.subscribe_to_messages(connection_name="eventReceiver")
        return ThreadEventManager(event_handler=event_handler)