from huma_sdk._session import _Session


def session(*args, **kwargs):
    session = _Session(*args, **kwargs)
    return session.create_connection(*args, **kwargs)