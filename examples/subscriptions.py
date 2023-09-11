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

    def fetch_subscription(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            subscription = self.subscribes_client.fetch_subscription(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
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


def main():
    subscribes_client = HumaSDKSubscribesClient()

    # Example usage
    subscribes_client.fetch_subscription(page=1, limit=50, sort_by=-1, order_by="", question="")

    ticket_number = "64d340834dd3067ec7d3a8eb"
    subscribes_client.create_subscription(ticket_number=ticket_number)

    subscribed_id = "6332d27a22e4200391f2c933"
    type = "<write one of the possible types>"    # visit documentation for more details
    subscribes_client.fetch_subscription_data(subscribed_id, page=1, limit=20, type=type)
    subscribes_client.delete_subscription(subscribed_id)

    question = "<write your question here>"
    subscribes_client.fetch_subscription_status(question)

if __name__ == "__main__":
    main()
