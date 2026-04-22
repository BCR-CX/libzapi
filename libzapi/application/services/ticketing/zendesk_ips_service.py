from libzapi.domain.models.ticketing.zendesk_ip import ZendeskIPs
from libzapi.infrastructure.api_clients.ticketing.zendesk_ip_api_client import ZendeskIPApiClient


class ZendeskIPsService:
    """High-level service using the API client."""

    def __init__(self, client: ZendeskIPApiClient) -> None:
        self._client = client

    def get_current(self) -> ZendeskIPs:
        return self._client.get()
