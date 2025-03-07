class AZEndpoint:
    """Represents the endpoint for the authorization server."""
    def __init__(self, endpoint: str, port: int):
        self.endpoint = endpoint  # The server endpoint address
        self.port = port          # The server port number


class AZConfig:
    """Configuration for the authorization client."""
    def __init__(self):
        self.pdp_endpoint = None  # Endpoint for the policy decision point, initially None


def with_endpoint(endpoint: str, port: int) -> callable:
    """Sets the gRPC endpoint for the authorization server."""
    def apply_option(config: AZConfig):
        config.pdp_endpoint = AZEndpoint(endpoint, port)
    return apply_option