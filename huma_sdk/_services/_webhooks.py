from huma_sdk.app import app


class _Webhooks:
    def __init__(self, *args, **kwargs):
        pass
    
    def activate_webhook_client(self, *args, **kwargs):
        app.run(*args, **kwargs)