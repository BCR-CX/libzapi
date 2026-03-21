from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.article_comment_cmds import (
    CreateArticleCommentCmd,
    UpdateArticleCommentCmd,
)
from libzapi.domain.models.help_center.article_comment import ArticleComment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.article_comment_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class ArticleCommentApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_by_article(self, article_id: int) -> Iterator[ArticleComment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/comments",
            base_url=self._http.base_url,
            items_key="comments",
        ):
            yield to_domain(data=obj, cls=ArticleComment)

    def list_by_user(self, user_id: int) -> Iterator[ArticleComment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/users/{int(user_id)}/comments",
            base_url=self._http.base_url,
            items_key="comments",
        ):
            yield to_domain(data=obj, cls=ArticleComment)

    def get(self, article_id: int, comment_id: int) -> ArticleComment:
        data = self._http.get(f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}")
        return to_domain(data=data["comment"], cls=ArticleComment)

    def create(self, article_id: int, cmd: CreateArticleCommentCmd) -> ArticleComment:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/help_center/articles/{int(article_id)}/comments", json=payload)
        return to_domain(data=data["comment"], cls=ArticleComment)

    def update(self, article_id: int, comment_id: int, cmd: UpdateArticleCommentCmd) -> ArticleComment:
        payload = to_payload_update(cmd)
        data = self._http.put(
            f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}", json=payload
        )
        return to_domain(data=data["comment"], cls=ArticleComment)

    def delete(self, article_id: int, comment_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/articles/{int(article_id)}/comments/{int(comment_id)}")
