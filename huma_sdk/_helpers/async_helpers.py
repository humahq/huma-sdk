import json
import os, websocket
from base64 import b64encode
from urllib.parse import urlparse
from huma_sdk._utils import parse_json_response
from huma_sdk.utils._log_utils import get_logger

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
                message_object = parse_json_response(message)
                message_payload = message_object['payload']['data'].get(connection_name)
                if callback(message_payload):
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
        return '''
            mutation newChat($topic: String!$agent: String) {
                newChat(topic: $topic, agent: $agent){
                    event_type
                    id
                    created_at
                    event_metadata{
                    event_message
                    event_data{
                        id
                        question_id
                        answer_id
                        question_version_number
                        is_visually_hidden
                        created_at
                        recepient
                        message_metadata{
                        focus
                        sources
                        processing_status{
                            state
                            reason
                        }
                        message_intent
                        answer_version_number
                        }
                        sub_message_metadata{
                        id
                        delta{
                            delta_data_type
                            delta_type
                            delta
                            created_at
                            updated_at
                        }
                        processing_status{
                            state
                            reason
                        }
                        readout_title
                        }
                    }
                    }
                    author{
                    role
                    tool
                    metadata
                    }
                    thread_metadata{
                    id
                    topic
                    users{
                        user_id
                        name
                        email
                        chat_role
                    }
                    agent
                    created_at
                    access_scope
                    is_pinned_chat
                            is_closed_chat
                    is_chat_processed
                    }
                }
                }
        '''

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
        return '''
            mutation sendMessage($chat_id: String!$is_new_chat: Boolean, $sources: [String], $focus: String, $message_intent: MessageIntent!, $user_message: UserMessageInput!, $message_id: String, $question_id: String) {
                sendMessage(chat_id: $chat_id, is_new_chat: $is_new_chat, sources: $sources, focus: $focus, message_intent: $message_intent, user_message: $user_message, message_id:$message_id, question_id: $question_id){
                    event_type
                    id
                    created_at
                    event_metadata{
                        event_message
                        event_data{
                            id
                            question_id
                            answer_id
                            question_version_number
                            is_visually_hidden
                            created_at
                            recepient
                            message_metadata{
                            focus
                            sources
                            processing_status{
                                state
                                reason
                            }
                            message_intent
                            answer_version_number
                            }
                            sub_message_metadata{
                            id
                            delta{
                                delta_data_type
                                delta_type
                                delta
                                created_at
                                updated_at
                            }
                            processing_status{
                                state
                                reason
                            }
                            readout_title
                            }
                        }
                    }
                    author{
                        role
                        tool
                        metadata
                    }
                    thread_metadata{
                        id
                        topic
                        users{
                            user_id
                            name
                            email
                            chat_role
                        }
                        agent
                        created_at
                        access_scope
                        is_pinned_chat
                        is_closed_chat
                        is_chat_processed
                    }
                }
            }
        '''

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

    def get_messages_v2():
        return '''
            query getMessages($chatId: String!, $page: Int, $limit: Int, $offset: Int) {
                getMessages(chat_id: $chatId, page:$page, limit: $limit, offset: $offset){
                    chat_details{
                    id
                    topic
                    users {
                        user_id
                        name
                        email
                        chat_role
                    }
                    agent
                    created_at
                    access_scope
                    is_closed_chat
                    is_chat_processed
                    is_pinned_chat
                    }
                    page
                    has_next_page
                    messages{
                    id
                    created_at
                    sender {
                        user_id
                        email
                        name
                        chat_role
                    }
                    focus
                    sources
                    message_versions {
                        id
                        created_at
                        user_message {
                        author {
                            role
                            tool
                            metadata
                        }
                        content {
                            type
                            message
                            metadata
                        }
                        metadata
                        }
                        message_intent
                        question_version_number
                        sender {
                        user_id
                        email
                        name
                        chat_role
                        }
                    }
                    response {
                        id
                        response_versions
                        parent_message_details {
                        id
                        created_at
                        user_message {
                        author {
                            role
                            tool
                            metadata
                        }
                        content {
                            type
                            message
                            metadata
                        }
                        metadata
                        }
                        message_intent
                        question_version_number
                        sender {
                        user_id
                        email
                        name
                        chat_role
                        }
                    }
                    response_component {
                        id
                        processing_status {
                        state
                        reason
                        }
                        answer_version_number
                        created_at
                        feedback {
                        text
                        reaction
                        }
                        fragments {
                        id
                        author {
                            role
                            tool
                            metadata
                        }
                        recepient
                        content
                        answer_id
                        sub_message_id
                        created_at
                        readout_title
                        processing_status {
                            state
                            reason
                        }
                        deltas {
                            delta_id
                            delta
                            delta_type
                            debug_logs {
                            debug_message
                            debug_type
                            debug_time
                            }
                            delta_data_type
                            created_at
                            updated_at
                        }
                        }
                    }
                    }
                    }
                }
            }
        '''

    def get_answer_data_v1(self, **kwargs):
        return '''
            query getAnswerData($utteranceId: String, $page: Int, $limit: Int) {
                getAnswerData(utteranceId: $utteranceId, page: $page, limit: $limit){
                    currentPage
                    hasNextPage
                    data
                }
            }
        '''

    def get_answer_data_v2(self, **kwargs):
        return '''
            query getAnswerData($utterance_id: String, $page: Int, $limit: Int) {
                getAnswerData(utterance_id: $utterance_id, page: $page, limit: $limti){
                    page
                    has_next_page
                    data
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

    def event_receiver_v2(self, **kwargs):
        return '''
            subscription EventReceiver {
                eventReceiver{
                    created_at
                    event_metadata {
                    event_data {
                        answer_id
                        created_at
                        id
                        is_visually_hidden
                        question_id
                        question_version_number
                        recepient
                        message_metadata {
                        answer_version_number
                        focus
                        message_intent
                        sources
                        processing_status {
                            reason
                            state
                        }
                        }
                        sub_message_metadata {
                        answer_version_number
                        id
                        readout_title
                        processing_status {
                            reason
                            state
                        }
                        delta {
                            created_at
                            delta
                            delta_data_type
                            delta_type
                            updated_at
                        }
                        }
                    }
                    event_message
                    }
                    event_type
                    id
                    thread_metadata {
                    access_scope
                    agent
                    created_at
                    id
                    is_chat_processed
                    is_closed_chat
                    is_pinned_chat
                    topic
                    users {
                        chat_role
                        email
                        name
                        user_id
                    }
                    }
                    author {
                    metadata
                    role
                    tool
                    }
                    content {
                    message
                    metadata
                    type
                    }
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
            ("GetMessages", "v2"): lambda: self.get_messages_v2(**kwargs),
            ("GetAnswerData", "v1"): lambda: self.get_answer_data_v1(**kwargs),
            ("GetAnswerData", "v2"): lambda: self.get_answer_data_v2(**kwargs),
            ("UpdateMessageSubscription", "v1"): lambda: self.update_message_subsciption_v1(**kwargs),
            ("UpdateMessageSubscription", "v2"): lambda: self.event_receiver_v2(**kwargs),
        }
        get_handler = mutation_handlers.get((type, version))
        return get_handler() if get_handler else ""