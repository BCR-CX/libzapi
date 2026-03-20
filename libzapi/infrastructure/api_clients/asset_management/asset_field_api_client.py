from __future__ import annotations
from typing import Iterable

from libzapi.domain.models.asset_management.asset_field import AssetField
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/it_asset_management/asset_types"


class AssetFieldApiClient:
    """HTTP adapter for Zendesk ITAM Asset Fields (read-only, nested under Asset Types).

    Note: The REST API only supports read operations for asset fields.
    Zendesk uses an internal GraphQL API for field mutations.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _path(self, asset_type_id: str, field_id: int | None = None) -> str:
        base = f"{_BASE}/{asset_type_id}/fields"
        if field_id is not None:
            return f"{base}/{int(field_id)}"
        return base

    def list(self, asset_type_id: str) -> Iterable[AssetField]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=self._path(asset_type_id),
            base_url=self._http.base_url,
            items_key="fields",
        ):
            yield to_domain(data=obj, cls=AssetField)

    def get(self, asset_type_id: str, field_id: int) -> AssetField:
        data = self._http.get(self._path(asset_type_id, field_id))
        return to_domain(data=data["field"], cls=AssetField)
