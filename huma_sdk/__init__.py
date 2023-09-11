from huma_sdk._session import _Session
__author__ = 'Huma AI'
__email__ = 'support@humaai.com'
__version__ = '0.1'


def session(*args, **kwargs):
    session = _Session(*args, **kwargs)
    return session.create_connection(*args, **kwargs)