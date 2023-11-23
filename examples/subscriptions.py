import time, json, os
from enum import Enum
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError

class HumaSDKSubscribesClient:
    def __init__(self):
        self.subscribes_client = huma_sdk.session(service_name="Subscriptions")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_subscriptions(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            subscription = self.subscribes_client.fetch_subscriptions(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            json_str = json.dumps(subscription, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def create_subscription(self, ticket_number: str=""):
        try:
            subscription = self.subscribes_client.create_subscription(ticket_number=ticket_number)
            json_str = json.dumps(subscription, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscription_data(self, subscribed_id: str="",page: int=1, limit: int=50, type:str="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            subscription = self.subscribes_client.fetch_subscription_data(subscribed_id,page=page,limit=limit,type=type, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            json_str = json.dumps(subscription, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return subscription
        except Exception as e:
            self.handle_exception(e)

    def delete_subscription(self, subscribed_id: str=""):
        try:
            subscription = self.subscribes_client.delete_subscription(subscribed_id)
            json_str = json.dumps(subscription, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscription_status(self, question: str=""):
        try:
            subscription = self.subscribes_client.fetch_subscription_status(question)
            json_str = json.dumps(subscription, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

class SubscriptionType(Enum):
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    BAR_CHART = "bar_chart"
    TABLE = "table"
    REPORT = "report"
    DASHBOARD = "dashboard"
    CHOROPLETH = "choropleth"
    MARKDOWN = "markdown"


def fetch_answer_data(subscribes_client: HumaSDKSubscribesClient, subscribed_id: str, page: int, limit: int, type: str, is_batch_pages: bool, max_page_count: int):
        try:
            result_response = subscribes_client.fetch_subscription_data(subscribed_id=subscribed_id, page=page, limit=limit, type=type, is_batch_pages=is_batch_pages, max_page_count=max_page_count)

            # Create 'output' directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save the result to a JSON file
            with open(f'output/{subscribed_id}_subscription_data.json', 'w') as f:
                json.dump(result_response, f, indent=4)

            print(f"Result saved to output/{subscribed_id}_subscription_data.json")

        except Exception as e:
            subscribes_client.handle_exception(e)


def main():
    subscribes_client = HumaSDKSubscribesClient()
    ticket_number = "<write your ticket number>"
    subscribed_id = "<write your subscribed question id>"
    question = "<write your question here>"

    #only applicable if response data is paginated
    page, limit = 1, 2
    max_page_count = 10
    is_batch_pages = bool(max_page_count)

    # Uncomment the function calls you want to execute
    subscribes_client.fetch_subscriptions(page=page, limit=limit, sort_by=-1, order_by="", question="", is_batch_pages=is_batch_pages, max_page_count=max_page_count)
    # subscribes_client.create_subscription(ticket_number=ticket_number)
    # fetch_answer_data(subscribes_client, subscribed_id=subscribed_id, page=page, limit=limit, type=SubscriptionType.TABLE.value, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
    # subscribes_client.delete_subscription(subscribed_id)
    # subscribes_client.fetch_subscription_status(question)

if __name__ == "__main__":
    main()
