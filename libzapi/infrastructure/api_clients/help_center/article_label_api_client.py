from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.article_label_cmds import CreateArticleLabelCmd
from libzapi.domain.models.help_center.article_label import ArticleLabel
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.article_label_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class ArticleLabelApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[ArticleLabel]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/help_center/articles/labels",
            base_url=self._http.base_url,
            items_key="labels",
        ):
            yield to_domain(data=obj, cls=ArticleLabel)

    def list_by_article(self, article_id: int) -> Iterator[ArticleLabel]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/labels",
            base_url=self._http.base_url,
            items_key="labels",
        ):
            yield to_domain(data=obj, cls=ArticleLabel)

    def get(self, article_id: int, label_id: int) -> ArticleLabel:
        data = self._http.get(f"/api/v2/help_center/articles/{int(article_id)}/labels/{int(label_id)}")
        return to_domain(data=data["label"], cls=ArticleLabel)

    def create(self, article_id: int, cmd: CreateArticleLabelCmd) -> ArticleLabel:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/help_center/articles/{int(article_id)}/labels", json=payload)
        return to_domain(data=data["label"], cls=ArticleLabel)

    def delete(self, article_id: int, label_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/articles/{int(article_id)}/labels/{int(label_id)}")
