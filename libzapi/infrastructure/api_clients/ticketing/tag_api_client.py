from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items


_RESOURCE_PATHS = {
    "ticket": "tickets",
    "user": "users",
    "organization": "organizations",
}


def _resource_path(resource: str, resource_id: int) -> str:
    if resource not in _RESOURCE_PATHS:
        raise ValueError(
            f"resource must be one of {sorted(_RESOURCE_PATHS)!r}, got {resource!r}"
        )
    return f"/api/v2/{_RESOURCE_PATHS[resource]}/{int(resource_id)}/tags"


class TagApiClient:
    """HTTP adapter for Zendesk Tags (account + per-resource)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_account(self) -> Iterator[dict]:
        yield from yield_items(
            get_json=self._http.get,
            first_path="/api/v2/tags",
            base_url=self._http.base_url,
            items_key="tags",
        )

    def list_for(self, resource: str, resource_id: int) -> list[str]:
        data = self._http.get(_resource_path(resource, resource_id))
        return list(data.get("tags", []))

    def add(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        data = self._http.put(
            _resource_path(resource, resource_id), {"tags": list(tags)}
        )
        return list(data.get("tags", []))

    def set(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        data = self._http.post(
            _resource_path(resource, resource_id), {"tags": list(tags)}
        )
        return list(data.get("tags", []))

    def remove(
        self, resource: str, resource_id: int, tags: Iterable[str]
    ) -> list[str]:
        data = self._http.delete(
            _resource_path(resource, resource_id),
            json={"tags": list(tags)},
        )
        return list((data or {}).get("tags", []))
