from typing import Iterable
from libzapi.application.commands.help_center.article_label_cmds import CreateArticleLabelCmd
from libzapi.domain.models.help_center.article_label import ArticleLabel
from libzapi.infrastructure.api_clients.help_center.article_label_api_client import ArticleLabelApiClient


class ArticleLabelsService:
    def __init__(self, client: ArticleLabelApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[ArticleLabel]:
        return self._client.list_all()

    def list_by_article(self, article_id: int) -> Iterable[ArticleLabel]:
        return self._client.list_by_article(article_id=article_id)

    def get(self, article_id: int, label_id: int) -> ArticleLabel:
        return self._client.get(article_id=article_id, label_id=label_id)

    def create(self, article_id: int, name: str) -> ArticleLabel:
        cmd = CreateArticleLabelCmd(name=name)
        return self._client.create(article_id=article_id, cmd=cmd)

    def delete(self, article_id: int, label_id: int) -> None:
        self._client.delete(article_id=article_id, label_id=label_id)
