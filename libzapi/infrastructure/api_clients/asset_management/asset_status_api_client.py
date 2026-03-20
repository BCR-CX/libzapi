from __future__ import annotations
from typing import Iterable

from libzapi.domain.models.asset_management.asset_status import AssetStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/it_asset_management/statuses"


class AssetStatusApiClient:
    """HTTP adapter for Zendesk ITAM Asset Statuses (read-only)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterable[AssetStatus]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="statuses",
        ):
            yield to_domain(data=obj, cls=AssetStatus)

    def get(self, status_id: str) -> AssetStatus:
        data = self._http.get(f"{_BASE}/{status_id}")
        return to_domain(data=data["status"], cls=AssetStatus)
