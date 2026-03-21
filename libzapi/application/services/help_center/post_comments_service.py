from typing import Iterable
from libzapi.application.commands.help_center.post_comment_cmds import CreatePostCommentCmd, UpdatePostCommentCmd
from libzapi.domain.models.help_center.post_comment import PostComment
from libzapi.infrastructure.api_clients.help_center.post_comment_api_client import PostCommentApiClient


class PostCommentsService:
    def __init__(self, client: PostCommentApiClient) -> None:
        self._client = client

    def list_by_post(self, post_id: int) -> Iterable[PostComment]:
        return self._client.list_by_post(post_id=post_id)

    def list_by_user(self, user_id: int) -> Iterable[PostComment]:
        return self._client.list_by_user(user_id=user_id)

    def get(self, post_id: int, comment_id: int) -> PostComment:
        return self._client.get(post_id=post_id, comment_id=comment_id)

    def create(self, post_id: int, body: str, notify_subscribers=True) -> PostComment:
        cmd = CreatePostCommentCmd(body=body, notify_subscribers=notify_subscribers)
        return self._client.create(post_id=post_id, cmd=cmd)

    def update(self, post_id: int, comment_id: int, body=None, official=None) -> PostComment:
        cmd = UpdatePostCommentCmd(body=body, official=official)
        return self._client.update(post_id=post_id, comment_id=comment_id, cmd=cmd)

    def delete(self, post_id: int, comment_id: int) -> None:
        self._client.delete(post_id=post_id, comment_id=comment_id)
