import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError
from enum import Enum


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
            print(subscription)
        except Exception as e:
            self.handle_exception(e)

    def create_subscription(self, ticket_number: str=""):
        try:
            subscription = self.subscribes_client.create_subscription(ticket_number=ticket_number)
            print(subscription)
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscription_data(self, subscribed_id: str="",page: int=1, limit: int=50, type:str=""):
        try:
            subscription = self.subscribes_client.fetch_subscription_data(subscribed_id,page=page,limit=limit,type=type)
            print(subscription)
        except Exception as e:
            self.handle_exception(e)

    def delete_subscription(self, subscribed_id: str=""):
        try:
            subscription = self.subscribes_client.delete_subscription(subscribed_id)
            print(subscription)
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscription_status(self, question: str=""):
        try:
            subscription = self.subscribes_client.fetch_subscription_status(question)
            print(subscription)
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

def main():
    subscribes_client = HumaSDKSubscribesClient()
    ticket_number = "<write your ticket number>"
    subscribed_id = "<write your subscribed question id>"
    question = "<write your question here>"

    # Uncomment the function calls you want to execute
    subscribes_client.fetch_subscriptions(page=1, limit=50, sort_by=-1, order_by="", question="")
    # subscribes_client.create_subscription(ticket_number=ticket_number)
    # subscribes_client.fetch_subscription_data(subscribed_id, page=1, limit=20, type=SubscriptionType.BAR_CHART.value)
    # subscribes_client.delete_subscription(subscribed_id)
    # subscribes_client.fetch_subscription_status(question)

if __name__ == "__main__":
    main()
