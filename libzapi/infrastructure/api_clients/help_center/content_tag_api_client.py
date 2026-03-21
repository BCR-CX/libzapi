from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.content_tag_cmds import CreateContentTagCmd, UpdateContentTagCmd
from libzapi.domain.models.help_center.content_tag import ContentTag
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.content_tag_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class ContentTagApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[ContentTag]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/guide/content_tags",
            base_url=self._http.base_url,
            items_key="content_tags",
        ):
            yield to_domain(data=obj, cls=ContentTag)

    def get(self, content_tag_id: str) -> ContentTag:
        data = self._http.get(f"/api/v2/guide/content_tags/{content_tag_id}")
        return to_domain(data=data["content_tag"], cls=ContentTag)

    def create(self, cmd: CreateContentTagCmd) -> ContentTag:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/guide/content_tags", json=payload)
        return to_domain(data=data["content_tag"], cls=ContentTag)

    def update(self, content_tag_id: str, cmd: UpdateContentTagCmd) -> ContentTag:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/guide/content_tags/{content_tag_id}", json=payload)
        return to_domain(data=data["content_tag"], cls=ContentTag)

    def delete(self, content_tag_id: str) -> None:
        self._http.delete(f"/api/v2/guide/content_tags/{content_tag_id}")
