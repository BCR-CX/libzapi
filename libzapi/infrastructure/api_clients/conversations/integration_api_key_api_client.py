from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.conversations.integration_api_key import IntegrationApiKey
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class IntegrationApiKeyApiClient:
    """HTTP adapter for Sunshine Conversations Integration API Keys."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, integration_id: str) -> Iterator[IntegrationApiKey]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/integrations/{integration_id}/keys",
            items_key="keys",
        ):
            yield to_domain(data=obj, cls=IntegrationApiKey)

    def get(self, app_id: str, integration_id: str, key_id: str) -> IntegrationApiKey:
        data = self._http.get(f"/v2/apps/{app_id}/integrations/{integration_id}/keys/{key_id}")
        return to_domain(data=data["key"], cls=IntegrationApiKey)

    def create(self, app_id: str, integration_id: str, display_name: str) -> IntegrationApiKey:
        data = self._http.post(
            f"/v2/apps/{app_id}/integrations/{integration_id}/keys",
            {"displayName": display_name},
        )
        return to_domain(data=data["key"], cls=IntegrationApiKey)

    def delete(self, app_id: str, integration_id: str, key_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/integrations/{integration_id}/keys/{key_id}")
