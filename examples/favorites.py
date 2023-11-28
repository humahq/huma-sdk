import time, json, os
from enum import Enum
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKFavoritesClient:
    def __init__(self):
        self.favorites_client = huma_sdk.session(service_name="Favorites")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def fetch_favorites(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            favorites = self.favorites_client.fetch_favorites(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            json_str = json.dumps(favorites, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def create_favorite(self, ticket_number: str=""):
        try:
            favorite = self.favorites_client.create_favorite(ticket_number=ticket_number)
            json_str = json.dumps(favorite, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def fetch_favorite_data(self, ticket_number: str="", page: int=1, limit: int=20, type: str="", is_batch_pages: bool=False, max_page_count: int=10):
        try:
            favorite = self.favorites_client.fetch_favorite_data(ticket_number, page=page, limit=limit, type=type, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
            json_str = json.dumps(favorite, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return favorite
        except Exception as e:
            self.handle_exception(e)

    def delete_favorite(self, ticket_number: str=""):
        try:
            favorite = self.favorites_client.delete_favorite(ticket_number)
            json_str = json.dumps(favorite, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

class FavoriteType(Enum):
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    BAR_CHART = "bar_chart"
    TABLE = "table"
    REPORT = "report"
    DASHBOARD = "dashboard"
    CHOROPLETH = "choropleth"
    MARKDOWN = "markdown"

def fetch_answer_data(favorites_client: HumaSDKFavoritesClient, ticket_number: str, page: int, limit: int, type: str, is_batch_pages: bool, max_page_count: int):
        try:
            result_response = favorites_client.fetch_favorite_data(ticket_number, page=page, limit=limit, type=type, is_batch_pages=is_batch_pages, max_page_count=max_page_count)

            # Create 'output' directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save the result to a JSON file
            with open(f'output/{ticket_number}_favorites_data.json', 'w') as f:
                json.dump(result_response, f, indent=4)

            print(f"Result saved to output/{ticket_number}_favorites_data.json")

        except Exception as e:
            favorites_client.handle_exception(e)


def main():
    favorites_client = HumaSDKFavoritesClient()
    ticket_number = "<write your ticket number>"

    #only applicable if response data is paginated
    page, limit = 1, 10
    max_page_count = 10
    is_batch_pages = bool(max_page_count)

    # Uncomment the function calls you want to execute
    favorites_client.fetch_favorites(page=page, limit=limit, sort_by=-1, order_by="", question="", is_batch_pages=is_batch_pages, max_page_count=max_page_count)
    # favorites_client.create_favorite(ticket_number=ticket_number)
    # fetch_answer_data(favorites_client, ticket_number, page=page, limit=limit, type=FavoriteType.TABLE.value, is_batch_pages=is_batch_pages, max_page_count=max_page_count)
    # favorites_client.delete_favorite(ticket_number=ticket_number)

if __name__ == "__main__":
    main()
