from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.conversations.app_key import AppKey
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class AppKeyApiClient:
    """HTTP adapter for Sunshine Conversations App Keys."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str) -> Iterator[AppKey]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/keys",
            items_key="keys",
        ):
            yield to_domain(data=obj, cls=AppKey)

    def get(self, app_id: str, key_id: str) -> AppKey:
        data = self._http.get(f"/v2/apps/{app_id}/keys/{key_id}")
        return to_domain(data=data["key"], cls=AppKey)

    def create(self, app_id: str, display_name: str) -> AppKey:
        data = self._http.post(f"/v2/apps/{app_id}/keys", {"displayName": display_name})
        return to_domain(data=data["key"], cls=AppKey)

    def delete(self, app_id: str, key_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/keys/{key_id}")
