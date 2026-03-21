from typing import Iterable
from libzapi.domain.models.help_center.article import Article
from libzapi.domain.models.help_center.post import Post
from libzapi.infrastructure.api_clients.help_center.search_api_client import SearchApiClient


class SearchService:
    def __init__(self, client: SearchApiClient) -> None:
        self._client = client

    def search_articles(self, query: str, **params: str) -> Iterable[Article]:
        return self._client.search_articles(query=query, **params)

    def search_posts(self, query: str, **params: str) -> Iterable[Post]:
        return self._client.search_posts(query=query, **params)
