from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.badge_category_cmds import CreateBadgeCategoryCmd
from libzapi.domain.models.help_center.badge_category import BadgeCategory
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.badge_category_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class BadgeCategoryApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[BadgeCategory]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/gather/badge_categories",
            base_url=self._http.base_url,
            items_key="badge_categories",
        ):
            yield to_domain(data=obj, cls=BadgeCategory)

    def get(self, badge_category_id: str) -> BadgeCategory:
        data = self._http.get(f"/api/v2/gather/badge_categories/{badge_category_id}")
        return to_domain(data=data["badge_category"], cls=BadgeCategory)

    def create(self, cmd: CreateBadgeCategoryCmd) -> BadgeCategory:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/gather/badge_categories", json=payload)
        return to_domain(data=data["badge_category"], cls=BadgeCategory)

    def delete(self, badge_category_id: str) -> None:
        self._http.delete(f"/api/v2/gather/badge_categories/{badge_category_id}")
