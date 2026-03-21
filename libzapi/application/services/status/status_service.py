from typing import Iterator

from libzapi.domain.models.status.incident import Incident
from libzapi.infrastructure.api_clients.status import StatusApiClient


class StatusService:
    """High-level service using the API client."""

    def __init__(self, client: StatusApiClient) -> None:
        self._client = client

    def list_active(self, subdomain: str | None = None) -> Iterator[Incident]:
        return self._client.list_active(subdomain=subdomain)

    def list_maintenance(self, subdomain: str | None = None) -> Iterator[Incident]:
        return self._client.list_maintenance(subdomain=subdomain)

    def get(self, incident_id: str) -> Incident:
        return self._client.get(incident_id=incident_id)
