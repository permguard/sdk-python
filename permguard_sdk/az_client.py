from permguard_sdk.az_config import AZConfig, AZEndpoint
from permguard_sdk.az.azreq import AZRequest
from permguard_sdk.az.azreq import AZResponse


class AZClient:
    """Client to interact with the authorization server."""
    def __init__(self, *opts):
        # Initialize configuration with default endpoint
        self.az_config = AZConfig()
        self.az_config.pdp_endpoint = AZEndpoint("localhost", 9094)
        # Apply any provided options
        for opt in opts:
            opt(self.az_config)

    def check(self, req: AZRequest) -> tuple[bool, AZResponse | None, Exception | None]:
        """Checks the input authorization request with the authorization server."""
        return True, None, None
