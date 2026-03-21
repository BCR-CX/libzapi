from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.help_center.article_cmds import CreateArticleCmd, UpdateArticleCmd
from libzapi.domain.models.help_center.article import Article
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.article_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class ArticleApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/help_center/articles",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def list_all_by_locale(self, locale: str) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/{locale}/articles",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def list_by_category(self, category_id: int) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/categories/{int(category_id)}/articles",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def list_by_section(self, section_id: int) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/sections/{int(section_id)}/articles",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def list_by_user(self, user_id: int) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/users/{int(user_id)}/articles",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def list_incremental(self, start_time: int) -> Iterator[Article]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/incremental?start_time={int(start_time)}",
            base_url=self._http.base_url,
            items_key="articles",
        ):
            yield to_domain(data=obj, cls=Article)

    def get(self, article_id: int) -> Article:
        data = self._http.get(f"/api/v2/help_center/articles/{int(article_id)}")
        return to_domain(data=data["article"], cls=Article)

    def create(self, section_id: int, cmd: CreateArticleCmd) -> Article:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/help_center/sections/{int(section_id)}/articles", json=payload)
        return to_domain(data=data["article"], cls=Article)

    def update(self, article_id: int, cmd: UpdateArticleCmd) -> Article:
        payload = to_payload_update(cmd)
        data = self._http.put(f"/api/v2/help_center/articles/{int(article_id)}", json=payload)
        return to_domain(data=data["article"], cls=Article)

    def delete(self, article_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/articles/{int(article_id)}")
