from typing import Iterator

from libzapi.domain.models.asset_management.asset_status import AssetStatus
from libzapi.infrastructure.api_clients.asset_management import AssetStatusApiClient


class AssetStatusesService:
    """High-level service using the API client."""

    def __init__(self, client: AssetStatusApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[AssetStatus]:
        return self._client.list()

    def get(self, status_id: str) -> AssetStatus:
        return self._client.get(status_id=status_id)
