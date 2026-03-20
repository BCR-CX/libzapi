from typing import Iterator

from libzapi.application.commands.asset_management.asset_cmds import CreateAssetCmd, UpdateAssetCmd
from libzapi.domain.models.asset_management.asset import Asset
from libzapi.infrastructure.api_clients.asset_management import AssetApiClient


class AssetsService:
    """High-level service using the API client."""

    def __init__(self, client: AssetApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[Asset]:
        return self._client.list()

    def get(self, asset_id: str) -> Asset:
        return self._client.get(asset_id=asset_id)

    def create(self, entity: CreateAssetCmd) -> Asset:
        return self._client.create(entity=entity)

    def update(self, asset_id: str, entity: UpdateAssetCmd) -> Asset:
        return self._client.update(asset_id=asset_id, entity=entity)

    def delete(self, asset_id: str) -> None:
        return self._client.delete(asset_id=asset_id)
