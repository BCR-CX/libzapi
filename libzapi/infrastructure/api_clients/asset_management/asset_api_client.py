from __future__ import annotations
from typing import Iterable

from libzapi.application.commands.asset_management.asset_cmds import CreateAssetCmd, UpdateAssetCmd
from libzapi.domain.models.asset_management.asset import Asset
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.asset_management.asset_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/it_asset_management/assets"


class AssetApiClient:
    """HTTP adapter for Zendesk ITAM Assets."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[Asset]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="assets",
        ):
            yield to_domain(data=obj, cls=Asset)

    def get(self, asset_id: str) -> Asset:
        data = self._http.get(f"{_BASE}/{asset_id}")
        return to_domain(data=data["asset"], cls=Asset)

    def create(self, entity: CreateAssetCmd) -> Asset:
        payload = to_payload_create(entity)
        data = self._http.post(_BASE, payload)
        return to_domain(data=data["asset"], cls=Asset)

    def update(self, asset_id: str, entity: UpdateAssetCmd) -> Asset:
        payload = to_payload_update(entity)
        data = self._http.patch(f"{_BASE}/{asset_id}", payload)
        return to_domain(data=data["asset"], cls=Asset)

    def delete(self, asset_id: str) -> None:
        self._http.delete(f"{_BASE}/{asset_id}")
