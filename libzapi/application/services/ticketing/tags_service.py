from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.infrastructure.api_clients.ticketing.tag_api_client import TagApiClient


class TagsService:
    """High-level service for Zendesk tags (account + per-resource)."""

    def __init__(self, client: TagApiClient) -> None:
        self._client = client

    def list_account(self) -> Iterator[dict]:
        return self._client.list_account()

    def list_for(self, resource: str, resource_id: int) -> list[str]:
        return self._client.list_for(resource=resource, resource_id=resource_id)

    def add(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        return self._client.add(
            resource=resource, resource_id=resource_id, tags=tags
        )

    def set(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        return self._client.set(
            resource=resource, resource_id=resource_id, tags=tags
        )

    def remove(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        return self._client.remove(
            resource=resource, resource_id=resource_id, tags=tags
        )
