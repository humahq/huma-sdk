import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKQuicklinksClient:
    def __init__(self):
        self.quicklinks_client = huma_sdk.session(service_name="Quicklinks")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_quicklinks(self):
        try:
            quicklinks = self.quicklinks_client.fetch_quicklinks()
            print(quicklinks)
        except Exception as e:
            self.handle_exception(e)


def main():
    quicklinks_client = HumaSDKQuicklinksClient()

    # Example usage
    quicklinks_client.fetch_quicklinks()

if __name__ == "__main__":
    main()
