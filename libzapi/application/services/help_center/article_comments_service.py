from typing import Iterable
from libzapi.application.commands.help_center.article_comment_cmds import (
    CreateArticleCommentCmd,
    UpdateArticleCommentCmd,
)
from libzapi.domain.models.help_center.article_comment import ArticleComment
from libzapi.infrastructure.api_clients.help_center.article_comment_api_client import ArticleCommentApiClient


class ArticleCommentsService:
    def __init__(self, client: ArticleCommentApiClient) -> None:
        self._client = client

    def list_by_article(self, article_id: int) -> Iterable[ArticleComment]:
        return self._client.list_by_article(article_id=article_id)

    def list_by_user(self, user_id: int) -> Iterable[ArticleComment]:
        return self._client.list_by_user(user_id=user_id)

    def get(self, article_id: int, comment_id: int) -> ArticleComment:
        return self._client.get(article_id=article_id, comment_id=comment_id)

    def create(
        self, article_id: int, body: str, locale=None, author_id=None, notify_subscribers=True
    ) -> ArticleComment:
        cmd = CreateArticleCommentCmd(
            body=body, locale=locale, author_id=author_id, notify_subscribers=notify_subscribers
        )
        return self._client.create(article_id=article_id, cmd=cmd)

    def update(self, article_id: int, comment_id: int, body=None) -> ArticleComment:
        cmd = UpdateArticleCommentCmd(body=body)
        return self._client.update(article_id=article_id, comment_id=comment_id, cmd=cmd)

    def delete(self, article_id: int, comment_id: int) -> None:
        self._client.delete(article_id=article_id, comment_id=comment_id)
