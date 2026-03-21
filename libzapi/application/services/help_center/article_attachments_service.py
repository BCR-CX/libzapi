from typing import Iterable

from libzapi.domain.models.help_center.article_attachment import ArticleAttachment
from libzapi.infrastructure.api_clients.help_center import ArticleAttachmentApiClient


class ArticleAttachmentsService:
    def __init__(self, client: ArticleAttachmentApiClient) -> None:
        self._client = client

    def list_all(self, article_id: int) -> Iterable[ArticleAttachment]:
        return self._client.list_all(article_id=article_id)

    def list_inline(self, article_id: int) -> Iterable[ArticleAttachment]:
        return self._client.list_inline(article_id=article_id)

    def list_block(self, article_id: int) -> Iterable[ArticleAttachment]:
        return self._client.list_block(article_id=article_id)

    def get(self, article_attachment_id: int) -> ArticleAttachment:
        return self._client.get(article_attachment_id=article_attachment_id)

    def create(self, article_id: int, file: tuple, inline: bool = False) -> ArticleAttachment:
        return self._client.create(article_id=article_id, file=file, inline=inline)

    def delete(self, article_attachment_id: int) -> None:
        self._client.delete(article_attachment_id=article_attachment_id)
