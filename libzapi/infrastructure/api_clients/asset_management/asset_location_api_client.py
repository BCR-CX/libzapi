from __future__ import annotations
from typing import Iterable

from libzapi.application.commands.asset_management.asset_location_cmds import (
    CreateAssetLocationCmd,
    UpdateAssetLocationCmd,
)
from libzapi.domain.models.asset_management.asset_location import AssetLocation
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.asset_management.asset_location_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/it_asset_management/locations"


class AssetLocationApiClient:
    """HTTP adapter for Zendesk ITAM Asset Locations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[AssetLocation]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="locations",
        ):
            yield to_domain(data=obj, cls=AssetLocation)

    def get(self, location_id: str) -> AssetLocation:
        data = self._http.get(f"{_BASE}/{location_id}")
        return to_domain(data=data["location"], cls=AssetLocation)

    def create(self, entity: CreateAssetLocationCmd) -> AssetLocation:
        payload = to_payload_create(entity)
        data = self._http.post(_BASE, payload)
        return to_domain(data=data["location"], cls=AssetLocation)

    def update(self, location_id: str, entity: UpdateAssetLocationCmd) -> AssetLocation:
        payload = to_payload_update(entity)
        data = self._http.patch(f"{_BASE}/{location_id}", payload)
        return to_domain(data=data["location"], cls=AssetLocation)

    def delete(self, location_id: str) -> None:
        self._http.delete(f"{_BASE}/{location_id}")
