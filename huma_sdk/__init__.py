_author__ = 'Huma AI'
__email__ = 'support@humaai.com'
__version__ = '0.2'
__all__ = ('huma-sdk',)

from huma_sdk._session import _Session


def session(*args, **kwargs):
    session = _Session(*args, **kwargs)
    return session.create_connection(*args, **kwargs)