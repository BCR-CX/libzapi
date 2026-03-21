from typing import Iterable
from libzapi.application.commands.help_center.post_cmds import CreatePostCmd, UpdatePostCmd
from libzapi.domain.models.help_center.post import Post
from libzapi.infrastructure.api_clients.help_center.post_api_client import PostApiClient


class PostsService:
    def __init__(self, client: PostApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Post]:
        return self._client.list_all()

    def list_by_topic(self, topic_id: int) -> Iterable[Post]:
        return self._client.list_by_topic(topic_id=topic_id)

    def list_by_user(self, user_id: int) -> Iterable[Post]:
        return self._client.list_by_user(user_id=user_id)

    def get(self, post_id: int) -> Post:
        return self._client.get(post_id=post_id)

    def create(self, title: str, details: str, topic_id: int, content_tag_ids=None, notify_subscribers=True) -> Post:
        cmd = CreatePostCmd(
            title=title,
            details=details,
            topic_id=topic_id,
            content_tag_ids=content_tag_ids,
            notify_subscribers=notify_subscribers,
        )
        return self._client.create(cmd=cmd)

    def update(self, post_id: int, title=None, details=None, topic_id=None, content_tag_ids=None) -> Post:
        cmd = UpdatePostCmd(title=title, details=details, topic_id=topic_id, content_tag_ids=content_tag_ids)
        return self._client.update(post_id=post_id, cmd=cmd)

    def delete(self, post_id: int) -> None:
        self._client.delete(post_id=post_id)
