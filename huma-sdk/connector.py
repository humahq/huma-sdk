import os
import json
import requests
from utils.log_utils import get_logger

class ApiConnector:
    def __init__(self, api_url=None, api_secret_key=None):
        self.api_url = api_url or os.environ.get("API_URL")
        self.api_secret_key = api_secret_key or os.environ.get("API_SECRET_KEY")
        self.logger = get_logger(__name__)

    def _handle_api_response(self, response):
        response_data = json.loads(response.text)
        if "error_message" in response_data:
            self.logger.error(f"Api Request Status: failed due to {response_data['error_message']}")
        return response_data
    
    def _make_request(self, **request_payload):
        try:
            response = requests.request(**request_payload)
            self.logger.info(f"Api Request Status: returned with {response.status_code} status code")
            return self._handle_api_response(response)

        except requests.ConnectionError as connection_error:
            self.logger.error(f"ConnectionError: {connection_error}")
            return {"error_message": f"ConnectionError: {connection_error}"}
        
        except requests.Timeout as timeout_error:
            self.logger.error(f"TimeoutError: {timeout_error}")
            return {"error_message": "Request timed out"}

    def _fetch_quicklinks(self):
        headers = {"Authorization": f"Bearer {self.api_secret_key}"}
        url = f"{self.api_url}/v1/quicklinks"
        return self._make_request(method="GET", url=url, headers=headers)

    def fetch_quicklinks(self):
        try:
            quicklinks = self._fetch_quicklinks()
            return quicklinks

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return {"error_message": f"An error occurred: {e}"}


if __name__ == "__main__":
# Usage:
    api_connector = ApiConnector(api_url=os.environ.get("API_URL"), api_secret_key=os.environ.get("API_SECRET_KEY"))
    quicklinks = api_connector.fetch_quicklinks()
    print(quicklinks)

    
