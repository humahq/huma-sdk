import os
import json
import requests
from utils.log_utils import get_logger

class Quicklinks:
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
    api_connector = Quicklinks(api_url=os.environ.get("API_URL"), api_secret_key=os.environ.get("API_SECRET_KEY"))
    quicklinks = api_connector.fetch_quicklinks()
    print(quicklinks)

class Audits:
    def __init__(self, api_url=None, api_secret_key=None):
        self.api_url = api_url or os.environ.get("API_URL")
        self.api_secret_key = api_secret_key or os.environ.get("API_SECRET_KEY")
        self.logger = get_logger(__name__)
        self._response_data = None

    def _handle_api_response(self, response):
        response_data = json.loads(response.text)
        if "error_message" in response_data:
            self.logger.error(f"API Request Status: failed due to {response_data['error_message']}")
        return response_data

    def _make_request(self, method, endpoint, headers=None, params=None):
        url = f"{self.api_url}{endpoint}"
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.api_secret_key}"

        try:
            response = requests.request(method, url, headers=headers, params=params)
            self.logger.info(f"API Request Status: returned with {response.status_code} status code")
            self._response_data = self._handle_api_response(response)
        except requests.RequestException as request_error:
            self.logger.error(f"RequestException: {request_error}")
            self._response_data = {"error_message": f"RequestException: {request_error}"}

    def get_audits(self):
        try:
            endpoint = "/v1/audits"
            self._make_request("GET", endpoint)
            return self._response_data
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return {"error_message": f"An error occurred: {e}"}

if __name__ == "__main__":
    sdk_connector = Audits(api_url=os.environ.get("API_URL"), api_secret_key=os.environ.get("API_SECRET_KEY"))
    audits = sdk_connector.get_audits()
    print("Audits:", audits)
    
    
class Aliases:
    def __init__(self, api_url=None, api_secret_key=None):
        self.api_url = api_url or os.environ.get("API_URL")
        self.api_secret_key = api_secret_key or os.environ.get("API_SECRET_KEY")
        self.logger = get_logger(__name__)
        self._response_data = None

    def _handle_api_response(self, response):
        response_data = json.loads(response.text)
        if "error_message" in response_data:
            self.logger.error(f"API Request Status: failed due to {response_data['error_message']}")
        return response_data

    def _make_request(self, method, endpoint, headers=None, params=None):
        url = f"{self.api_url}{endpoint}"
        headers = headers or {}
        headers["Authorization"] = f"Bearer {self.api_secret_key}"

        try:
            response = requests.request(method, url, headers=headers, params=params)
            self.logger.info(f"API Request Status: returned with {response.status_code} status code")
            self._response_data = self._handle_api_response(response)
        except requests.RequestException as request_error:
            self.logger.error(f"RequestException: {request_error}")
            self._response_data = {"error_message": f"RequestException: {request_error}"}

    def get_aliases(self):
        try:
            endpoint = "/v1/aliases"
            self._make_request("GET", endpoint)
            return self._response_data
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            return {"error_message": f"An error occurred: {e}"}

if __name__ == "__main__":
    sdk_connector = Aliases(api_url=os.environ.get("API_URL"), api_secret_key=os.environ.get("API_SECRET_KEY"))
    aliases = sdk_connector.get_aliases()
    print("Aliases:", aliases)


