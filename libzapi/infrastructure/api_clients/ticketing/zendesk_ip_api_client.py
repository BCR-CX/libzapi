from __future__ import annotations

from libzapi.domain.models.ticketing.zendesk_ip import ZendeskIPs
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


class ZendeskIPApiClient:
    """HTTP adapter for Zendesk Public IPs"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> ZendeskIPs:
        data = self._http.get("/api/v2/ips.json")
        return to_domain(data=data, cls=ZendeskIPs)
