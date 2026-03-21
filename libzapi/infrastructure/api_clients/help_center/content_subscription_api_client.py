from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.content_subscription_cmds import CreateContentSubscriptionCmd
from libzapi.domain.models.help_center.content_subscription import ContentSubscription
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.content_subscription_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class ContentSubscriptionApiClient:
    _PREFIX_MAP = {
        "articles": "/api/v2/help_center/articles",
        "sections": "/api/v2/help_center/sections",
        "topics": "/api/v2/community/topics",
        "posts": "/api/v2/community/posts",
    }

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _base(self, content_type: str, content_id: int) -> str:
        return f"{self._PREFIX_MAP[content_type]}/{int(content_id)}/subscriptions"

    def list(self, content_type: str, content_id: int) -> Iterator[ContentSubscription]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=self._base(content_type, content_id),
            base_url=self._http.base_url,
            items_key="subscriptions",
        ):
            yield to_domain(data=obj, cls=ContentSubscription)

    def get(self, content_type: str, content_id: int, subscription_id: int) -> ContentSubscription:
        data = self._http.get(f"{self._base(content_type, content_id)}/{int(subscription_id)}")
        return to_domain(data=data["subscription"], cls=ContentSubscription)

    def create(self, content_type: str, content_id: int, cmd: CreateContentSubscriptionCmd) -> ContentSubscription:
        payload = to_payload_create(cmd)
        data = self._http.post(self._base(content_type, content_id), json=payload)
        return to_domain(data=data["subscription"], cls=ContentSubscription)

    def delete(self, content_type: str, content_id: int, subscription_id: int) -> None:
        self._http.delete(f"{self._base(content_type, content_id)}/{int(subscription_id)}")
