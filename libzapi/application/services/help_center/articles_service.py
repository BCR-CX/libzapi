from typing import Iterable

from libzapi.application.commands.help_center.article_cmds import CreateArticleCmd, UpdateArticleCmd
from libzapi.domain.models.help_center.article import Article
from libzapi.infrastructure.api_clients.help_center import ArticleApiClient


class ArticlesService:
    def __init__(self, client: ArticleApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Article]:
        return self._client.list_all()

    def list_all_by_locale(self, locale: str) -> Iterable[Article]:
        return self._client.list_all_by_locale(locale=locale)

    def list_by_category(self, category_id: int) -> Iterable[Article]:
        return self._client.list_by_category(category_id=category_id)

    def list_by_section(self, section_id: int) -> Iterable[Article]:
        return self._client.list_by_section(section_id=section_id)

    def list_by_user(self, user_id: int) -> Iterable[Article]:
        return self._client.list_by_user(user_id=user_id)

    def list_incremental(self, start_time: int) -> Iterable[Article]:
        return self._client.list_incremental(start_time=start_time)

    def get(self, article_id: int) -> Article:
        return self._client.get(article_id=article_id)

    def create(self, section_id: int, title: str, body: str, locale: str = "en-us", **kwargs) -> Article:
        cmd = CreateArticleCmd(title=title, body=body, locale=locale, **kwargs)
        return self._client.create(section_id=section_id, cmd=cmd)

    def update(self, article_id: int, **kwargs) -> Article:
        cmd = UpdateArticleCmd(**kwargs)
        return self._client.update(article_id=article_id, cmd=cmd)

    def delete(self, article_id: int) -> None:
        self._client.delete(article_id=article_id)
