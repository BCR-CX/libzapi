from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.conversations.client import Client
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class ClientApiClient:
    """HTTP adapter for Sunshine Conversations Clients."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, user_id_or_external_id: str) -> Iterator[Client]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/users/{user_id_or_external_id}/clients",
            items_key="clients",
        ):
            yield to_domain(data=obj, cls=Client)

    def create(self, app_id: str, user_id_or_external_id: str, payload: dict) -> Client:
        data = self._http.post(f"/v2/apps/{app_id}/users/{user_id_or_external_id}/clients", payload)
        return to_domain(data=data["client"], cls=Client)

    def remove(self, app_id: str, user_id_or_external_id: str, client_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/users/{user_id_or_external_id}/clients/{client_id}")
