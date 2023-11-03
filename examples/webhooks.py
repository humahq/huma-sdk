import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


class HumaSDKWebhooksClient:
    def __init__(self):
        self.webhooks_client = huma_sdk.session(service_name="Webhooks")

    def handle_exception(self, exception):
        if isinstance(exception, UnauthorizedException):
            print("Unauthorized:", exception)
        elif isinstance(exception, ResourceNotExistsError):
            print("Resource Not Exists:", exception)
        else:
            print("An unexpected error occurred:", exception)

    def activate_webhook_client(self, debug: bool=True, port: int=5000):
        try:
            self.webhooks_client.activate_webhook_client(debug=debug, port=port)
        except Exception as e:
            self.handle_exception(e)


def main():
    webhooks_client = HumaSDKWebhooksClient()

    # Example usage
    debug: bool = "<Whether to enable debug mode>"
    port: int = "<write port number to use>"
    webhooks_client.activate_webhook_client(debug=True, port=5001)

if __name__ == "__main__":
    main()