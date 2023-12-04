import uvicorn
from huma_sdk.app import app
from asgiref.wsgi import WsgiToAsgi
from werkzeug.middleware.dispatcher import DispatcherMiddleware


class _Webhooks:
    def __init__(self, *args, **kwargs):
        pass

    def activate_webhook_client(self, port):
        wsgi_app = DispatcherMiddleware(app)
        asgi_app = WsgiToAsgi(wsgi_app)
        uvicorn.run(asgi_app, host="0.0.0.0", port=port)