import json
from base64 import b64encode
from urllib.parse import urlparse
import requests, threading, time, os, websocket
from huma_sdk.utils._log_utils import get_logger
from huma_sdk._utils import parse_json_response

# Constants
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


class SubscriptionClient:
    def __init__(self, api_secret_key=None, **kwargs) -> None:
        self.api_secret_key = api_secret_key or os.environ.get('API_SECRET_KEY')
        self.graphql_api_url = kwargs.get('graphql_api_url') or os.environ.get('GRAPHQL_API_URL')
        self.logger = get_logger(__name__)

    def construct_subscription_query(self, subscription_query, variables):
        """
        Construct a GraphQL subscription query.

        Args:
            subscription_query (str): The GraphQL subscription query string.
            variables (dict): The variables to be included in the subscription query.

        Returns:
            str: The JSON-encoded subscription query.
        """
        return json.dumps({ "query" : subscription_query, "variables" : variables })

    def on_open(self, ws):
        """
        Callback function to handle WebSocket opening event.

        Args:
            ws (websocket.WebSocketApp): The WebSocketApp instance.
        """
        self.logger.info(f"{GREEN}Connection built{RESET}")
        init = {'type': 'connection_init',"payload": {"connectionTimeoutMs":300000000}}
        init_conn = json.dumps(init)
        ws.send(init_conn)

    def on_error(self, ws, error):
        """
        Callback function to handle WebSocket error event.

        Args:
            ws (websocket.WebSocketApp): The WebSocketApp instance.
            error (str): The error message.
        """
        self.logger.error(f"{RED}Error{RESET}")

    def on_close(self, ws, close_status_code, close_msg):
        """
        Callback function to handle WebSocket closing event.

        Args:
            ws (websocket.WebSocketApp): The WebSocketApp instance.
        """
        self.logger.info(f"{YELLOW}Connection closed! {RESET}")

    def create_on_message(self, subscription_query, variables, callback, connection_name):
        """
        Create a callback function to handle WebSocket message event.

        Args:
            subscription_query (str): The GraphQL subscription query string.
            variables (dict): The variables to be included in the subscription query.
            callback (function): The callback function to process the subscription data.

        Returns:
            function: A function to handle WebSocket messages.
        """
        def on_message(ws, message):
            """
            Handle WebSocket message event.

            Args:
                ws (websocket.WebSocketApp): The WebSocketApp instance.
                message (str): The received message.
            """
            message_object = parse_json_response(message)
            message_type   = message_object['type']

            if( message_type == 'connection_ack' ):
                register = {
                    "id": "1",
                    'type': 'start',
                    "payload": {
                        "data": self.construct_subscription_query(subscription_query, variables),
                        "extensions": {
                            "authorization": {
                                "host": self.extract_host(),
                                "authorization": self.api_secret_key
                            }
                        }
                    },
                }
                start_sub = json.dumps(register)
                ws.send(start_sub)

            elif(message_type == 'data'):
                is_chat_processed, chat_id = None, None
                message_object = parse_json_response(message)
                message_payload = message_object['payload']['data'].get(connection_name)

                if message_payload.get("contentType") == "system" and message_payload.get("contentsubType") in ["system", "blocking"]:
                    message_content_json = parse_json_response(message_payload.get("content"))
                    is_chat_processed = message_content_json.get("is_processed")
                    chat_id = message_content_json.get("chat_id")

                callback(message_payload)

                if is_chat_processed:
                    ws.close()

        return on_message

    def extract_host(self):
        """
        Extract the host from the AppSync URL stored in environment variables.

        Returns:
            str: The host part of the AppSync URL.
        """
        parsed_url = urlparse(self.graphql_api_url)
        return parsed_url.netloc

    def get_api_header(self):
        return {
            "host": self.extract_host(),
            "authorization": self.api_secret_key
        }

    def encode_header(self, header_obj):
        """
        Encode the header object to a base64-encoded string.

        Args:
            header_obj (dict): The header object to be encoded.

        Returns:
            str: The base64-encoded header string.
        """
        return b64encode(json.dumps(header_obj).encode('utf-8')).decode('utf-8')

    def construct_ws_connection_url(self):
        """
        Construct the WebSocket connection URL.

        Returns:
            str: The WebSocket connection URL.
        """
        ws_url = self.graphql_api_url.replace("https", "wss") + "/realtime"
        header = self.encode_header(self.get_api_header())
        connection_url = f"{ws_url}?header={header}&payload=e30="
        return connection_url

    def subscription_thread(self, subscription_query, variables, callback, connection_name):
        """
        Create and run a WebSocket subscription thread.

        Args:
            subscription_query (str): The GraphQL subscription query string.
            variables (dict): The variables to be included in the subscription query.
            callback (function): The callback function to process the subscription data.
        """
        ws_url = self.construct_ws_connection_url()
        ws = websocket.WebSocketApp(
            ws_url,
            subprotocols=["graphql-ws"],
            on_open = self.on_open,
            on_message = self.create_on_message(subscription_query, variables, callback, connection_name),
            on_error = self.on_error,
            on_close = self.on_close
        )
        ws.run_forever()

class AppsyncSchemaClient:
    def __init__(self, *args, **kwargs): ...

    def new_chat_mutation_v1(self, **kwargs):
        topic = kwargs.get('topic')
        return f'''
            mutation {{
                newChat(topic: "{topic or 'New Chat'}") {{
                    id
                }}
            }}
        '''

    def new_chat_mutation_v2(self, **kwargs):
        ...

    def send_message_mutation_v1(self, **kwargs):
        return '''
            mutation MyMutation(
                $chatId: String = "",
                $message: MessageInput
            ) {
                sendMessage(
                    chatId: $chatId,
                    message: $message
                ) {
                    id
                    createdAt
                    contentType
                    content
                    chatId
                    isNewChat
                    is_processed
                    messageId
                    userId
                    sender {
                        email
                        id
                        name
                    }
                }
            }
        '''

    def send_message_mutation_v2(self, **kwargs):
        ...

    def process_utterance_v1(self, **kwargs):
        return '''
            mutation MyMutation(
                $chatId: String!,
                $utterance: String!,
                $respondingToMessageId: String!
            ) {
                processUtterance(
                    chatId: $chatId
                    utterance: $utterance
                    respondingToMessageId: $respondingToMessageId
                )
            }
        '''

    def get_messages_v1(self, **kwargs):
        return '''
            query getMessages($chatId: String!, $type: MessageStatus, $limit: Int) {
                getMessages(chatId: $chatId, type: $type, limit: $limit) {
                    currentPage
                    hasNextPage
                    is_chat_processed
                    message {
                        chatId
                        createdAt
                        id
                        is_processed
                        isStoppedChat
                        sub_messages {
                            debug_and_status_state
                            debug_and_status_title
                            chatId
                            content
                            contentType
                            createdAt
                            id
                            messageId
                            debug_and_status {
                                content
                                contentsubType
                                createdAt
                                debuglogs {
                                    content
                                    createdAt
                                    is_error
                                }
                                id
                                sub_message_id
                            }
                        }
                        sender {
                            email
                            id
                            name
                        }
                    }
                }
            }
        '''

    def update_message_subsciption_v1(self, **kwargs):
        return '''
            subscription SubscribeUpdateMessage($chatId: String!) {
                subscribeUpdateMessage(chatId: $chatId) {
                    chatId
                    content
                    contentType
                    contentsubType
                    createdAt
                    id
                    messageId
                    status
                    statusId
                    debug_and_status_state
                    debug_and_status_title
                    isStoppedChat
                }
            }
        '''

    def get_schema(self, type: str="", version: str="", **kwargs):
        mutation_handlers = {
            ("NewChat", "v1"): lambda: self.new_chat_mutation_v1(**kwargs),
            ("NewChat", "v2"): lambda: self.new_chat_mutation_v2(**kwargs),
            ("SendMessage", "v1"): lambda: self.send_message_mutation_v1(**kwargs),
            ("SendMessage", "v2"): lambda: self.send_message_mutation_v2(**kwargs),
            ("ProcessUtterance", "v1"): lambda: self.process_utterance_v1(**kwargs),
            ("GetMessages", "v1"): lambda: self.get_messages_v1(**kwargs),
            ("UpdateMessageSubscription", "v1"): lambda: self.update_message_subsciption_v1(**kwargs),
        }
        get_handler = mutation_handlers.get((type, version))
        return get_handler() if get_handler else ""


class _AsyncServices(SubscriptionClient, AppsyncSchemaClient):
    def __init__(self, service_name=None, api_version=None, **kwargs):
        self.service_name = service_name
        self.api_version = api_version or "v1"
        self.chat_id = None
        self.message_id = None
        self.should_stop = False  # Variable to control the loop
        self.final_messages = None  # Variable to store final messages

        super().__init__(**kwargs)

    def get_headers(self):
        return { 'authorization': f"Bearer {self.api_secret_key}" }

    def error(self, error):
        raise Exception(error)

    def execute_gql(self, query, variables=None):
        data = {
            'query': query,
            'variables': variables,
        }
        response = requests.post(self.graphql_api_url, headers=self.get_headers(), json=data)
        return response.json()

    def process_utterance(self, message_content):
        query =self.get_schema(type="ProcessUtterance", version=self.api_version)
        variables = {"chatId": self.chat_id, "respondingToMessageId": self.message_id, "utterance": message_content}
        response = self.execute_gql(query, variables)
        return response

    def start_new_chat(self, topic=None):
        query = self.get_schema(type="NewChat", version=self.api_version, topic=topic)
        response = self.execute_gql(query)
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
        submit_message = self.process_utterance(message_content) # This submit message to UP queue for processing

    def handle_subscription(self, subscription_query, variables, callback, connection_name):
        threading.Thread(target=self.subscription_thread, args=(subscription_query, variables, callback, connection_name)).start()

    def on_update_message(self, data):
        message = data
        # self.logger.info(f"Message update received: {message['content']}")
        if message['contentType'] == "stream" or (message['contentType'] == "analyser" and message['contentsubType'] == "visual"):
            print(f"{GREEN}{message['content']}{RESET}")

    def get_message(self, chat_id):
        query = self.get_schema(type="GetMessages", api_version=self.api_version)
        variables = {
            "chatId": chat_id,
            "limit": 1,
            "type": "status",
        }
        response = self.execute_gql(query, variables)
        return response


    def subscribe_to_messages(self):
        subscription_schema = self.get_schema(type="UpdateMessageSubscription", version=self.api_version)
        variables = { "chatId": self.chat_id }
        self.handle_subscription(
            subscription_schema, variables,
            self.on_update_message, connection_name="subscribeUpdateMessage"
        )

    def ask_question(self, question: str, thread_id: str, topic: str=None):
        if not thread_id:
            self.start_new_chat(topic=topic or question)
        else:
            response = self.get_message(thread_id)
            if not response:
                return Exception("Wrong thread Id")
            else:
                self.chat_id = thread_id

        self.send_message(message_content=question)
        self.subscribe_to_messages()

    def new_chat(self, topic: str):
        self.start_new_chat(topic=topic)
        return self.chat_id

    def _make_async_request(self, question: str, topic: str=None, thread_id: str=""):
        if self.service_name == "Questions":
            self.ask_question(question, thread_id, topic)
            return "SUCCEEDED"
        elif self.service_name == "Threads":
            self.new_chat(topic=topic or question)
            return self.chat_id