from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.post_comment_cmds import CreatePostCommentCmd, UpdatePostCommentCmd
from libzapi.domain.models.help_center.post_comment import PostComment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.post_comment_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class PostCommentApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_by_post(self, post_id: int) -> Iterator[PostComment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/posts/{int(post_id)}/comments",
            base_url=self._http.base_url,
            items_key="comments",
        ):
            yield to_domain(data=obj, cls=PostComment)

    def list_by_user(self, user_id: int) -> Iterator[PostComment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/community/users/{int(user_id)}/comments",
            base_url=self._http.base_url,
            items_key="comments",
        ):
            yield to_domain(data=obj, cls=PostComment)

    def get(self, post_id: int, comment_id: int) -> PostComment:
        data = self._http.get(f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}")
        return to_domain(data=data["comment"], cls=PostComment)

    def create(self, post_id: int, cmd: CreatePostCommentCmd) -> PostComment:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/community/posts/{int(post_id)}/comments", json=payload)
        return to_domain(data=data["comment"], cls=PostComment)

    def update(self, post_id: int, comment_id: int, cmd: UpdatePostCommentCmd) -> PostComment:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}", json=payload)
        return to_domain(data=data["comment"], cls=PostComment)

    def delete(self, post_id: int, comment_id: int) -> None:
        self._http.delete(f"/api/v2/community/posts/{int(post_id)}/comments/{int(comment_id)}")
