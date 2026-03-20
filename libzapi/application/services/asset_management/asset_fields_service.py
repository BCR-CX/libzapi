from typing import Iterator

from libzapi.domain.models.asset_management.asset_field import AssetField
from libzapi.infrastructure.api_clients.asset_management import AssetFieldApiClient


class AssetFieldsService:
    """High-level service using the API client (read-only)."""

    def __init__(self, client: AssetFieldApiClient) -> None:
        self._client = client

    def list_all(self, asset_type_id: str) -> Iterator[AssetField]:
        return self._client.list(asset_type_id=asset_type_id)

    def get(self, asset_type_id: str, field_id: int) -> AssetField:
        return self._client.get(asset_type_id=asset_type_id, field_id=field_id)
