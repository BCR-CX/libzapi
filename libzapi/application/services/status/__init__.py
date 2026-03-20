from libzapi.application.services.status.status_service import StatusService
from libzapi.infrastructure.http.client import HttpClient
import libzapi.infrastructure.api_clients.status as api

_DEFAULT_BASE_URL = "https://status.zendesk.com"


class ZendeskStatus:
    """SDK entry point for Zendesk Status API (public, no auth required)."""

    def __init__(self, base_url: str = _DEFAULT_BASE_URL):
        http = HttpClient(base_url, headers={})
        self.incidents = StatusService(api.StatusApiClient(http))
