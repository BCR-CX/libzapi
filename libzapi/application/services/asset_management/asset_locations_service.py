from typing import Iterator

from libzapi.application.commands.asset_management.asset_location_cmds import (
    CreateAssetLocationCmd,
    UpdateAssetLocationCmd,
)
from libzapi.domain.models.asset_management.asset_location import AssetLocation
from libzapi.infrastructure.api_clients.asset_management import AssetLocationApiClient


class AssetLocationsService:
    """High-level service using the API client."""

    def __init__(self, client: AssetLocationApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[AssetLocation]:
        return self._client.list()

    def get(self, location_id: str) -> AssetLocation:
        return self._client.get(location_id=location_id)

    def create(self, entity: CreateAssetLocationCmd) -> AssetLocation:
        return self._client.create(entity=entity)

    def update(self, location_id: str, entity: UpdateAssetLocationCmd) -> AssetLocation:
        return self._client.update(location_id=location_id, entity=entity)

    def delete(self, location_id: str) -> None:
        return self._client.delete(location_id=location_id)
