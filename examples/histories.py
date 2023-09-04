import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKHistoriesClient:
    def __init__(self):
        self.histories_client = huma_sdk.session(service_name="Histories")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_history(self, page: int=1, limit: int=20, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            history = self.histories_client.fetch_history(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
            print(history)
        except Exception as e:
            self.handle_exception(e)

    def fetch_history_data(self, ticket_number: str="", page: int=1, limit: int=10, type: str=""):
        try:
            history_data = self.histories_client.fetch_history_data(ticket_number, page=page, limit=limit, type=type)
            print(history_data)
        except Exception as e:
            self.handle_exception(e)

    def submit_history_visual(self, ticket_number, file_type, visual_type):
        try:
            submission_status = self.histories_client.submit_history_visual(ticket_number=ticket_number, file_type=file_type, visual_type=visual_type)
            print(submission_status)
        except Exception as e:
            self.handle_exception(e)

    def check_history_visual_status(self, conversion_id: str=""):
        try:
            conversion_status = self.histories_client.check_history_visual_status(conversion_id)
            print(conversion_status)
        except Exception as e:
            self.handle_exception(e)

    def fetch_history_visual_result(self, conversion_id: str=""):
        try:
            history_visual = self.histories_client.fetch_history_visual_result(conversion_id)
            print(history_visual)
        except Exception as e:
            self.handle_exception(e)


def main():
    history_client = HumaSDKHistoriesClient()

    # Example usage
    history_client.fetch_history(page=1, limit=20, sort_by=-1, order_by="", question="")

    ticket_number = "<write your ticket number>"
    type = "<write one of the possible types>"    # visit documentation for more details
    history_client.fetch_history_data(ticket_number, page=1, limit=10, type=type)

    file_type = "<write your required file type>"
    visual_type = "<write one of the possible types>"   # visit documentation for more detailss
    history_client.submit_history_visual(ticket_number=ticket_number, file_type=file_type, visual_type=visual_type)

    conversion_id = "<write your conversion id"
    history_client.check_history_visual_status(conversion_id)
    history_client.fetch_history_visual_result(conversion_id)

if __name__ == "__main__":
    main()
