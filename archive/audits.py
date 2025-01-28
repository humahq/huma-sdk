import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

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

    def fetch_audits(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", endpoint: str="", content: str="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            kwargs = dict(page=page, limit=limit, sort_by=sort_by, order_by=order_by, endpoint=endpoint, content=content, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            audits = self.audits_client.fetch_audits(**kwargs)
            json_str = json.dumps(audits, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)


def main():
    audit_client = HumaSDKAuditsClient()

    #only applicable if response data is paginated
    page, limit = 1, 10
    max_page_count = 10
    is_batch_pages = bool(max_page_count)

    # Example usage
    content = "<write content to search>"
    endpoint = "<write name of the endpoint to search>"
    audit_client.fetch_audits(page=page, limit=limit, sort_by=-1, order_by="", endpoint=endpoint, content=content, is_batch_pages=is_batch_pages, max_page_count=max_page_count)

if __name__ == "__main__":
    main()
