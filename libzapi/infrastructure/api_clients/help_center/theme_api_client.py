from __future__ import annotations
from typing import Iterator
from libzapi.domain.models.help_center.theme import Theme
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class ThemeApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Theme]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/guide/theming/themes",
            base_url=self._http.base_url,
            items_key="themes",
        ):
            yield to_domain(data=obj, cls=Theme)

    def get(self, theme_id: str) -> Theme:
        data = self._http.get(f"/api/v2/guide/theming/themes/{theme_id}")
        return to_domain(data=data["theme"], cls=Theme)

    def publish(self, theme_id: str) -> Theme:
        data = self._http.post(f"/api/v2/guide/theming/themes/{theme_id}/publish", json={})
        return to_domain(data=data["theme"], cls=Theme)

    def delete(self, theme_id: str) -> None:
        self._http.delete(f"/api/v2/guide/theming/themes/{theme_id}")
