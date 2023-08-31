import huma_sdk
from huma_sdk.exceptions import UnauthorizedException, ResourceNotExistsError


def fetch_quicklinks():
    try:
        quicklinks_client = huma_sdk.session(service_name="Quicklinks")
        quicklinks = quicklinks_client.fetch_quicklinks()
        print(quicklinks)
    except UnauthorizedException as e:
        print(e)
    except ResourceNotExistsError as e:
        print(e)
    except Exception as e:
        print(e)


def fetch_audits():
    try:
        quicklinks_client = huma_sdk.session(service_name="Audits")
        quicklinks = quicklinks_client.fetch_audits()
        print(quicklinks)
    except UnauthorizedException as e:
        print(e)
    except ResourceNotExistsError as e:
        print(e)
    except Exception as e:
        print(e)


def fetch_aliases():
    try:
        quicklinks_client = huma_sdk.session(service_name="Aliases")
        quicklinks = quicklinks_client.fetch_aliases()
        print(quicklinks)
    except UnauthorizedException as e:
        print(e)
    except ResourceNotExistsError as e:
        print(e)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    fetch_quicklinks()
    fetch_aliases()