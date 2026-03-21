from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.post_cmds import CreatePostCmd, UpdatePostCmd
from libzapi.domain.models.help_center.post import Post
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.post_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class PostApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Post]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/community/posts",
            base_url=self._http.base_url,
            items_key="posts",
        ):
            yield to_domain(data=obj, cls=Post)

    def list_by_topic(self, topic_id: int) -> Iterator[Post]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/topics/{int(topic_id)}/posts",
            base_url=self._http.base_url,
            items_key="posts",
        ):
            yield to_domain(data=obj, cls=Post)

    def list_by_user(self, user_id: int) -> Iterator[Post]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/users/{int(user_id)}/posts",
            base_url=self._http.base_url,
            items_key="posts",
        ):
            yield to_domain(data=obj, cls=Post)

    def get(self, post_id: int) -> Post:
        data = self._http.get(f"/api/v2/community/posts/{int(post_id)}")
        return to_domain(data=data["post"], cls=Post)

    def create(self, cmd: CreatePostCmd) -> Post:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/community/posts", json=payload)
        return to_domain(data=data["post"], cls=Post)

    def update(self, post_id: int, cmd: UpdatePostCmd) -> Post:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/community/posts/{int(post_id)}", json=payload)
        return to_domain(data=data["post"], cls=Post)

    def delete(self, post_id: int) -> None:
        self._http.delete(f"/api/v2/community/posts/{int(post_id)}")
