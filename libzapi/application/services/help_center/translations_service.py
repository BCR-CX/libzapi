from __future__ import annotations
from typing import Iterable
from libzapi.application.commands.help_center.translation_cmds import CreateTranslationCmd, UpdateTranslationCmd
from libzapi.domain.models.help_center.translation import Translation
from libzapi.infrastructure.api_clients.help_center.translation_api_client import TranslationApiClient


class TranslationsService:
    def __init__(self, client: TranslationApiClient) -> None:
        self._client = client

    def list(self, content_type: str, content_id: int) -> Iterable[Translation]:
        return self._client.list(content_type=content_type, content_id=content_id)

    def get(self, content_type: str, content_id: int, locale: str) -> Translation:
        return self._client.get(content_type=content_type, content_id=content_id, locale=locale)

    def list_missing(self, content_type: str, content_id: int) -> list[str]:
        return self._client.list_missing(content_type=content_type, content_id=content_id)

    def create(
        self,
        content_type: str,
        content_id: int,
        locale: str,
        title: str,
        body: str,
        draft: bool = False,
        outdated: bool = False,
    ) -> Translation:
        cmd = CreateTranslationCmd(locale=locale, title=title, body=body, draft=draft, outdated=outdated)
        return self._client.create(content_type=content_type, content_id=content_id, cmd=cmd)

    def update(
        self, content_type: str, content_id: int, locale: str, title=None, body=None, draft=None, outdated=None
    ) -> Translation:
        cmd = UpdateTranslationCmd(title=title, body=body, draft=draft, outdated=outdated)
        return self._client.update(content_type=content_type, content_id=content_id, locale=locale, cmd=cmd)

    def delete(self, translation_id: int) -> None:
        self._client.delete(translation_id=translation_id)
