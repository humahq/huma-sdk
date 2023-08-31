import os
import json
import requests
from huma_sdk.utils._log_utils import get_logger
from huma_sdk.exceptions import UnauthorizedException
from huma_sdk._utils import parse_json_response


class _Services():
    def __init__(self, service_name=None, api_url=None, api_secret_key=None):
        self.api_url = api_url or os.environ.get('API_URL')
        self.api_secret_key = api_secret_key or os.environ.get('API_SECRET_KEY')
        self.service_name = service_name
        self.test_url = f"{self.api_url}/v1/sdk/access-permissions"
        self.logger = get_logger(__name__)
        self.test_connection()

    def _handle_api_response(self, response):
        response_data = parse_json_response(response.text)

        if response.status_code == 401:
            error_message = response_data.get('error_message')
            self.logger.error(f"Unauthorized Exception: {error_message}")
            raise UnauthorizedException(service_name=self.service_name, error_message=error_message)

        if "error_message" in response_data:
            self.logger.info(f"Request Status: returned with {response.status_code} status code")
            self.logger.error(f"Request Status: failed due to {response_data['error_message']}")

        return response_data

    def _make_request(self, **request_payload):
        try:
            response = requests.request(**request_payload)
            return self._handle_api_response(response)

        except requests.ConnectionError as connection_error:
            self.logger.error(f"ConnectionError: {connection_error}")
            return {"error_message": f"ConnectionError: {connection_error}"}

        except requests.Timeout as timeout_error:
            self.logger.error(f"TimeoutError: {timeout_error}")
            return {"error_message": "Request timed out"}

    def test_connection(self):
        headers = {
            "Authorization": f"Bearer {self.api_secret_key}",
            "Service-access": self.service_name
        }
        return self._make_request(method="GET", url=self.test_url, headers=headers)


if __name__ == "__main__":
    service_client = _Services(service_name="questions",api_url=os.environ.get('API_URL'), api_secret_key=os.environ.get('API_SECRET_KEY'))
    response = service_client._make_request(method="GET", url=service_client.api_url)
    print(response)