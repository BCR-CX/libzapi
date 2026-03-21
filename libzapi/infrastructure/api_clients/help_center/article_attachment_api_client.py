from __future__ import annotations

from typing import Iterator

from libzapi.domain.models.help_center.article_attachment import ArticleAttachment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class ArticleAttachmentApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, article_id: int) -> Iterator[ArticleAttachment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/attachments",
            base_url=self._http.base_url,
            items_key="article_attachments",
        ):
            yield to_domain(data=obj, cls=ArticleAttachment)

    def list_inline(self, article_id: int) -> Iterator[ArticleAttachment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/attachments/inline",
            base_url=self._http.base_url,
            items_key="article_attachments",
        ):
            yield to_domain(data=obj, cls=ArticleAttachment)

    def list_block(self, article_id: int) -> Iterator[ArticleAttachment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/articles/{int(article_id)}/attachments/block",
            base_url=self._http.base_url,
            items_key="article_attachments",
        ):
            yield to_domain(data=obj, cls=ArticleAttachment)

    def get(self, article_attachment_id: int) -> ArticleAttachment:
        data = self._http.get(f"/api/v2/help_center/articles/attachments/{int(article_attachment_id)}")
        return to_domain(data=data["article_attachment"], cls=ArticleAttachment)

    def create(self, article_id: int, file: tuple, inline: bool = False) -> ArticleAttachment:
        path = f"/api/v2/help_center/articles/{int(article_id)}/attachments"
        files = {"file": file}
        data_fields = {"inline": str(inline).lower()} if inline else None
        data = self._http.post_multipart(path, files=files, data=data_fields)
        return to_domain(data=data["article_attachment"], cls=ArticleAttachment)

    def delete(self, article_attachment_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/articles/attachments/{int(article_attachment_id)}")
