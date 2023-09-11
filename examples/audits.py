import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKAuditsClient:
    def __init__(self):
        self.audits_client = huma_sdk.session(service_name="Audits")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_audits(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", endpoint: str="", content: str=""):
        try:
            audits = self.audits_client.fetch_audits(page=page, limit=limit, sort_by=sort_by, order_by=order_by, endpoint=endpoint, content=content)
            print(audits)
        except Exception as e:
            self.handle_exception(e)


def main():
    audit_client = HumaSDKAuditsClient()

    # Example usage
    content = "<write content to search>"
    endpoint = "<write name of the endpoint to search>"
    audit_client.fetch_audits(page=1, limit=50, sort_by=-1, order_by="", endpoint=endpoint, content=content)

if __name__ == "__main__":
    main()
