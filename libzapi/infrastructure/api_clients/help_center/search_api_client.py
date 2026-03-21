from __future__ import annotations
from typing import Iterator
from libzapi.domain.models.help_center.article import Article
from libzapi.domain.models.help_center.post import Post
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class SearchApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def search_articles(self, query: str, **params: str) -> Iterator[Article]:
        parts = [f"query={query}"] + [f"{k}={v}" for k, v in params.items()]
        qs = "&".join(parts)
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/search?{qs}",
            base_url=self._http.base_url,
            items_key="results",
        ):
            yield to_domain(data=obj, cls=Article)

    def search_posts(self, query: str, **params: str) -> Iterator[Post]:
        parts = [f"query={query}"] + [f"{k}={v}" for k, v in params.items()]
        qs = "&".join(parts)
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/community_posts/search?{qs}",
            base_url=self._http.base_url,
            items_key="results",
        ):
            yield to_domain(data=obj, cls=Post)
