import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKSubscribesClient:
    def __init__(self):
        self.subscribes_client = huma_sdk.session(service_name="Subscribes")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_subscribes(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            subscribes = self.subscribes_client.fetch_subscribes(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
            print(subscribes)
        except Exception as e:
            self.handle_exception(e)

    def create_subscribe(self, ticket_number: str=""):
        try:
            subscribe = self.subscribes_client.create_subscribe(ticket_number=ticket_number)
            print(subscribe)
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscribe_data(self, subscribed_id: str=""):
        try:
            subscribe = self.subscribes_client.fetch_subscribe_data(subscribed_id)
            print(subscribe)
        except Exception as e:
            self.handle_exception(e)

    def delete_subscribe(self, subscribed_id: str=""):
        try:
            subscribe = self.subscribes_client.delete_subscribe(subscribed_id)
            print(subscribe)
        except Exception as e:
            self.handle_exception(e)

    def fetch_subscribed_status(self, question: str=""):
        try:
            subscribe = self.subscribes_client.fetch_subscribed_status(question)
            print(subscribe)
        except Exception as e:
            self.handle_exception(e)


def main():
    subscribes_client = HumaSDKSubscribesClient()

    # Example usage
    subscribes_client.fetch_subscribes(page=1, limit=50, sort_by=-1, order_by="", question="")

    ticket_number = "<write your ticket number>"
    subscribes_client.create_subscribe(ticket_number=ticket_number)

    subscribed_id = "<write your subscribed id>"
    type = "<write one of the possible types>"    # visit documentation for more details
    subscribes_client.fetch_subscribe_data(subscribed_id, page=1, limit=20, type=type)
    subscribes_client.delete_subscribe(subscribed_id)

    question = "<write your question here>"
    subscribes_client.fetch_subscribed_status(question)

if __name__ == "__main__":
    main()
