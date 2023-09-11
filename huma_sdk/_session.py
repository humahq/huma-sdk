from huma_sdk._service_config import SERVICE_MAPPINGS, AVAILABLE_SERVICES
from huma_sdk.exceptions import ResourceNotExistsError

class _Session():
    def __init__(self, *args, **kwargs):
        self.service_name = kwargs.get('service_name')
        self.available_services = AVAILABLE_SERVICES
        if not self.service_name or self.service_name not in self.available_services:
            raise ResourceNotExistsError(self.service_name, available_services=self.available_services)

    def create_connection(self, *args, **kwargs):
        return SERVICE_MAPPINGS.get(self.service_name)(*args, **kwargs)