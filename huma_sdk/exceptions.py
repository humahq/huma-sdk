class ResourceNotExistsError(Exception):
    """Raised when you attempt to create a resource that does not exist."""
    def __init__(self, service_name, available_services):
        msg = (
            "The '{}' resource does not exist.\n"
            "The available resources are:\n"
            "   - {}\n".format(
                service_name, '\n   - '.join(available_services)
            )
        )
        super().__init__(msg)


class UnauthorizedException(Exception):
    def __init__(self, service_name, error_message) -> None:
        msg = (
            f"Access to the '{service_name}' service is restricted due to {error_message}"
        )
        super().__init__(msg)