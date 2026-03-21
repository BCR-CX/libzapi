from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.topic_cmds import CreateTopicCmd, UpdateTopicCmd
from libzapi.domain.models.help_center.topic import Topic
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.topic_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class TopicApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Topic]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/community/topics",
            base_url=self._http.base_url,
            items_key="topics",
        ):
            yield to_domain(data=obj, cls=Topic)

    def get(self, topic_id: int) -> Topic:
        data = self._http.get(f"/api/v2/community/topics/{int(topic_id)}")
        return to_domain(data=data["topic"], cls=Topic)

    def create(self, cmd: CreateTopicCmd) -> Topic:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/community/topics", json=payload)
        return to_domain(data=data["topic"], cls=Topic)

    def update(self, topic_id: int, cmd: UpdateTopicCmd) -> Topic:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/community/topics/{int(topic_id)}", json=payload)
        return to_domain(data=data["topic"], cls=Topic)

    def delete(self, topic_id: int) -> None:
        self._http.delete(f"/api/v2/community/topics/{int(topic_id)}")
