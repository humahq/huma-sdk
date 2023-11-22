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

    def fetch_subscriptions(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            subscription = self.subscribes_client.fetch_subscriptions(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
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

    def fetch_subscription_data(self, subscribed_id: str="",page: int=1, limit: int=50, type:str=""):
        try:
            subscription = self.subscribes_client.fetch_subscription_data(subscribed_id,page=page,limit=limit,type=type)
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

def example_fetch_subscription_data(subscribes_client: HumaSDKSubscribesClient, subscribed_id: str, type: str, max_page_count: int = 10, limit: str = 25):
    try:
        # Initial fetch
        result_response = subscribes_client.fetch_subscription_data(subscribed_id=subscribed_id, limit=limit, type=type)

        if 'metadata' in result_response:
            answer_data = result_response.get('subscriptions', {}).get('data', [])
            total_records_present = result_response['metadata'].get('total_count', 0)
            print(f"Total records present: {total_records_present}")
            pages_to_fetch = min(max_page_count, result_response['metadata'].get('page_count', 0))
            total_records = min(pages_to_fetch * int(limit), result_response['metadata'].get('total_count', 0))
            if total_records < total_records_present:
                print(f"Restricting total records to {total_records} only because max_page_count is set to {max_page_count} with per page limit as {limit}.")

            print(f"Successfully fetched {limit} records out of {total_records}. Fetching records for page 2.")
            print("Next fetch in 5 seconds...")
            time.sleep(5)

            # Fetch additional pages
            for page in range(2, pages_to_fetch + 1):
                page_limit = result_response['metadata'].get('per_page')
                result_response = subscribes_client.fetch_subscription_data(page=page, limit=page_limit, subscribed_id=subscribed_id)
                new_data = result_response.get('subscriptions', {}).get('data', [])
                answer_data.extend(new_data)

                if page != pages_to_fetch:
                    print(f"Successfully fetched {(page) * page_limit} records out of {total_records}. Fetching records for page {page + 1}.")
                    print("Next fetch in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Successfully fetched {(page) * page_limit} records out of {total_records}.")

            # Update the response structure
            result_response['subscriptions']['data'] = answer_data
            del result_response['metadata']

        # Create 'output' directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

        # Save the result to a JSON file
        with open(f'output/{subscribed_id}_subscription_data.json', 'w') as f:
            json.dump(result_response, f, indent=4)

    except Exception as e:
        subscribes_client.handle_exception(e)


def main():
    subscribes_client = HumaSDKSubscribesClient()
    ticket_number = "<write your ticket number>"
    subscribed_id = "<write your subscribed question id>"
    question = "<write your question here>"

    #only applicable if answer data is paginated
    max_page_count = "<write maximum required pages>"
    limit = "<write limit of each page>"

    # Uncomment the function calls you want to execute
    subscribes_client.fetch_subscriptions(page=1, limit=50, sort_by=-1, order_by="", question="")
    # subscribes_client.create_subscription(ticket_number=ticket_number)
    # example_fetch_subscription_data(subscribes_client=subscribes_client, subscribed_id=subscribed_id, type=SubscriptionType.TABLE.value, max_page_count=max_page_count, limit=limit)
    # subscribes_client.delete_subscription(subscribed_id)
    # subscribes_client.fetch_subscription_status(question)

if __name__ == "__main__":
    main()
