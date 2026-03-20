from __future__ import annotations
from typing import Iterable

from libzapi.application.commands.asset_management.asset_type_cmds import CreateAssetTypeCmd, UpdateAssetTypeCmd
from libzapi.domain.models.asset_management.asset_type import AssetType
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.asset_management.asset_type_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/it_asset_management/asset_types"


class AssetTypeApiClient:
    """HTTP adapter for Zendesk ITAM Asset Types."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[AssetType]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="asset_types",
        ):
            yield to_domain(data=obj, cls=AssetType)

    def get(self, asset_type_id: str) -> AssetType:
        data = self._http.get(f"{_BASE}/{asset_type_id}")
        return to_domain(data=data["asset_type"], cls=AssetType)

    def create(self, entity: CreateAssetTypeCmd) -> AssetType:
        payload = to_payload_create(entity)
        data = self._http.post(_BASE, payload)
        return to_domain(data=data["asset_type"], cls=AssetType)

    def update(self, asset_type_id: str, entity: UpdateAssetTypeCmd) -> AssetType:
        payload = to_payload_update(entity)
        data = self._http.patch(f"{_BASE}/{asset_type_id}", payload)
        return to_domain(data=data["asset_type"], cls=AssetType)

    def delete(self, asset_type_id: str) -> None:
        self._http.delete(f"{_BASE}/{asset_type_id}")
