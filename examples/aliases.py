import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKAliasClient:
    def __init__(self):
        self.aliases_client = huma_sdk.session(service_name="Aliases")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_aliases(self, page=1, limit=50, sort_by=-1, order_by="", search_by="", search_for=""):
        try:
            aliases = self.aliases_client.fetch_aliases(page=page, limit=limit, sort_by=sort_by, order_by=order_by, search_by=search_by, search_for=search_for)
            print(aliases)
        except Exception as e:
            self.handle_exception(e)


def main():
    alias_client = HumaSDKAliasClient()

    # Example usage
    alias_client.fetch_aliases(page=1, limit=50, sort_by=-1, order_by="", search_by="", search_for="")

if __name__ == "__main__":
    main()
