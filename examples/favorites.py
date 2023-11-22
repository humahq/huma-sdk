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

    def fetch_favorites(self, page: int=1, limit: int=50, sort_by: int=-1, order_by: str="", question: str=""):
        try:
            favorites = self.favorites_client.fetch_favorites(page=page, limit=limit, sort_by=sort_by, order_by=order_by, question=question)
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

    def fetch_favorite_data(self, ticket_number: str="", page: int=1, limit: int=20, type: str=""):
        try:
            favorite = self.favorites_client.fetch_favorite_data(ticket_number, page=page, limit=limit, type=type)
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


def example_fetch_favorites(favorites_client):
    favorites_client.fetch_favorites(page=1, limit=50, sort_by=-1, order_by="", question="")

def example_create_favorite(favorites_client, ticket_number):
    favorites_client.create_favorite(ticket_number=ticket_number)

def example_delete_favorite(favorites_client, ticket_number):
    favorites_client.delete_favorite(ticket_number=ticket_number)

def example_fetch_favorite_data(favorites_client: HumaSDKFavoritesClient, ticket_number: str, type: str, max_page_count: int=10, limit: int=25):
        try:
            result_response = favorites_client.fetch_favorite_data(ticket_number=ticket_number, limit=limit, type=type)

            if 'metadata' in result_response:
                answer_data = result_response.get('answer', {}).get('data', [])
                total_records_present = result_response['metadata'].get('total_count', 0)
                print(f"Total records present: {total_records_present}")
                pages_to_fetch = min(max_page_count, result_response['metadata'].get('page_count', 0))
                total_records = min(pages_to_fetch * int(limit), result_response['metadata'].get('total_count', 0))
                if total_records < total_records_present:
                    print(f"Restricting total records to {total_records} only because max_page_count is set to {max_page_count} with per page limit as {limit}.")

                print(f"Successfully fetched {limit} records out of {total_records}. Fetching records for page 2.")
                print("Next fetch in 5 seconds...")
                time.sleep(5)

                # Fetch additional pages
                for page in range(2, pages_to_fetch + 1):
                    page_limit = result_response['metadata'].get('per_page')
                    result_response = favorites_client.fetch_favorite_data(page=page, limit=page_limit, ticket_number=ticket_number)
                    new_data = result_response.get('answer', {}).get('data', [])
                    answer_data.extend(new_data)

                    if page != pages_to_fetch:
                        print(f"Successfully fetched {(page) * page_limit} records out of {total_records}. Fetching records for page {page + 1}.")
                        print("Next fetch in 5 seconds...")
                        time.sleep(5)
                    else:
                        print(f"Successfully fetched {(page) * page_limit} records out of {total_records}.")

                # Update the response structure
                result_response['answer']['data'] = answer_data
                del result_response['metadata']

            # Create 'output' directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            # Save the result to a JSON file
            with open(f'output/{ticket_number}_favorite_data.json', 'w') as f:
                json.dump(result_response, f, indent=4)

        except Exception as e:
            favorites_client.handle_exception(e)


def main():
    favorites_client = HumaSDKFavoritesClient()
    ticket_number = "<write your ticket number>"

    #only applicable if answer data is paginated
    max_page_count = 3 or "<write maximum required pages>"  
    limit = 1 or "<write limit of each page>"

    # Uncomment the function calls you want to execute
    example_fetch_favorites(favorites_client)
    # example_create_favorite(favorites_client, ticket_number)
    # example_fetch_favorite_data(favorites_client, ticket_number, FavoriteType.TABLE.value, max_page_count=max_page_count, limit=limit)
    # example_delete_favorite(favorites_client, ticket_number)

if __name__ == "__main__":
    main()
