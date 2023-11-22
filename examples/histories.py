import time
import json
import os
from enum import Enum

import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


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
            json_str = json.dumps(history, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
        except Exception as e:
            self.handle_exception(e)

    def fetch_history_data(self, ticket_number: str="", page: int=1, limit: int=10, type: str=""):
        try:
            history_data = self.histories_client.fetch_history_data(ticket_number, page=page, limit=limit, type=type)
            json_str = json.dumps(history_data, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return history_data
        except Exception as e:
            self.handle_exception(e)

    def submit_history_visual(self, ticket_number, file_type, visual_type):
        try:
            submission_status = self.histories_client.submit_history_visual(ticket_number=ticket_number, file_type=file_type, visual_type=visual_type)
            json_str = json.dumps(submission_status, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return submission_status
        except Exception as e:
            self.handle_exception(e)

    def check_history_visual_status(self, conversion_id: str=""):
        try:
            conversion_status = self.histories_client.check_history_visual_status(conversion_id)
            json_str = json.dumps(conversion_status, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return conversion_status
        except Exception as e:
            self.handle_exception(e)

    def fetch_history_visual_result(self, conversion_id: str=""):
        try:
            history_visual = self.histories_client.fetch_history_visual_result(conversion_id)
            json_str = json.dumps(history_visual, indent=4)
            print(highlight(json_str, JsonLexer(), TerminalFormatter()))
            return history_visual
        except Exception as e:
            self.handle_exception(e)

class VisualType(Enum):
    LINE_CHART = "line_chart"
    PIE_CHART = "pie_chart"
    BAR_CHART = "bar_chart"
    TABLE = "table"
    REPORT = "report"
    DASHBOARD = "dashboard"
    CHOROPLETH = "choropleth"
    MARKDOWN = "markdown"

class FileType(Enum):
    CSV = "csv"
    PPTX = "pptx"
    PDF = "pdf"

def download_history_visual(history_client, ticket_number, file_type, visual_type):
    submission_status = history_client.submit_history_visual(ticket_number=ticket_number, file_type=file_type, visual_type=visual_type)
    conversion_id = submission_status.get('conversion_id')

    if 'error_message' in submission_status:
        print(f'Failed to submit question, because {submission_status["error_message"]}')
        return

    while True:
        print(f"Checking Status of '{conversion_id}' conversion id")
        history_visual_status = history_client.check_history_visual_status(conversion_id)

        conversion_status = history_visual_status.get('status', '')
        if conversion_status == 'succeeded':
            print(f"Getting visual of answer with '{conversion_id}' conversion id")
            result_response = history_client.fetch_history_visual_result(conversion_id)

            if not os.path.exists("output"):
                os.mkdir("output")

            with open(f'output/{conversion_id}_visual.json', 'w') as f:
                json.dump(result_response, f, indent=4)

            print(f'Copy the link from the result and paste in your favorite browser for downloading the visual file')
            print(f"Result saved to output/{conversion_id}_visual.json")
            break
        elif conversion_status == 'rejected':
            print(f'The history answer with "{conversion_id}" conversion id failed to process.')
            break
        else:
            print(f'History answer with "{conversion_id}" conversion id is being processed, checking status in 5 seconds...')
            time.sleep(5)


def fetch_answer_data(history_client: HumaSDKHistoriesClient, ticket_number: str, type: str, max_page_count: int=10, limit: int=25):
        try:
            result_response = history_client.fetch_history_data(ticket_number=ticket_number, limit=limit, type=type)

            if 'metadata' in result_response:
                #validating max_page_count
                if not isinstance(max_page_count, int):
                    max_page_count = 3

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
                    result_response = history_client.fetch_history_data(page=page, limit=page_limit, ticket_number=ticket_number)
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
            with open(f'output/{ticket_number}_history_data.json', 'w') as f:
                json.dump(result_response, f, indent=4)

        except Exception as e:
            history_client.handle_exception(e)


def main():
    history_client = HumaSDKHistoriesClient()
    ticket_number = "<write your ticket number>"

    #only applicable if answer data is paginated
    max_page_count = "<write maximum required pages>"
    limit = 10

    # Uncomment the function calls you want to execute
    history_client.fetch_history(page=1, limit=20, sort_by=-1, order_by="", question="")

    # Example: Fetch history data
    # fetch_answer_data(history_client, ticket_number, type=VisualType.TABLE.value, max_page_count=max_page_count, limit=limit)

    # Example: Download history visual file
    # download_history_visual(history_client, ticket_number, FileType.PPTX.value, VisualType.BAR_CHART.value)

if __name__ == "__main__":
    main()
