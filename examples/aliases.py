import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

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

    def fetch_aliases(self, page=1, limit=50, sort_by=-1, order_by="", search_by="", search_for="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            kwargs = dict(page=page, limit=limit, sort_by=sort_by, order_by=order_by, search_by=search_by, search_for=search_for, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            aliases = self.aliases_client.fetch_aliases(**kwargs)
            json_str = json.dumps(aliases, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)


def main():
    alias_client = HumaSDKAliasClient()

    #only applicable if response data is paginated
    page, limit = 1, 5
    max_page_count = 10
    is_batch_pages = bool(max_page_count)

    # Example usage
    alias_client.fetch_aliases(page=page, limit=limit, sort_by=-1, order_by="", search_by="", search_for="", is_batch_pages=is_batch_pages, max_page_count=max_page_count)

if __name__ == "__main__":
    main()
