from typing import Iterator

from libzapi.application.commands.asset_management.asset_type_cmds import CreateAssetTypeCmd, UpdateAssetTypeCmd
from libzapi.domain.models.asset_management.asset_type import AssetType
from libzapi.infrastructure.api_clients.asset_management import AssetTypeApiClient


class AssetTypesService:
    """High-level service using the API client."""

    def __init__(self, client: AssetTypeApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[AssetType]:
        return self._client.list()

    def get(self, asset_type_id: str) -> AssetType:
        return self._client.get(asset_type_id=asset_type_id)

    def create(self, entity: CreateAssetTypeCmd) -> AssetType:
        return self._client.create(entity=entity)

    def update(self, asset_type_id: str, entity: UpdateAssetTypeCmd) -> AssetType:
        return self._client.update(asset_type_id=asset_type_id, entity=entity)

    def delete(self, asset_type_id: str) -> None:
        return self._client.delete(asset_type_id=asset_type_id)
