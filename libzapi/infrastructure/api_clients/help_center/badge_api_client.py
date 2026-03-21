from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.badge_cmds import CreateBadgeCmd, UpdateBadgeCmd
from libzapi.domain.models.help_center.badge import Badge
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.badge_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class BadgeApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Badge]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/gather/badges",
            base_url=self._http.base_url,
            items_key="badges",
        ):
            yield to_domain(data=obj, cls=Badge)

    def get(self, badge_id: str) -> Badge:
        data = self._http.get(f"/api/v2/gather/badges/{badge_id}")
        return to_domain(data=data["badge"], cls=Badge)

    def create(self, cmd: CreateBadgeCmd) -> Badge:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/gather/badges", json=payload)
        return to_domain(data=data["badge"], cls=Badge)

    def update(self, badge_id: str, cmd: UpdateBadgeCmd) -> Badge:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/gather/badges/{badge_id}", json=payload)
        return to_domain(data=data["badge"], cls=Badge)

    def delete(self, badge_id: str) -> None:
        self._http.delete(f"/api/v2/gather/badges/{badge_id}")
