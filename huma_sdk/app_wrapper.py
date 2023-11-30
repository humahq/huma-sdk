from werkzeug.middleware.dispatcher import DispatcherMiddleware
from asgiref.wsgi import WsgiToAsgi
from huma_sdk.app import app  # Import your Flask app

wsgi_app = DispatcherMiddleware(app)
asgi_app = WsgiToAsgi(wsgi_app)

