from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.translation_cmds import CreateTranslationCmd, UpdateTranslationCmd
from libzapi.domain.models.help_center.translation import Translation
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.translation_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class TranslationApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, content_type: str, content_id: int) -> Iterator[Translation]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/help_center/{content_type}/{int(content_id)}/translations",
            base_url=self._http.base_url,
            items_key="translations",
        ):
            yield to_domain(data=obj, cls=Translation)

    def get(self, content_type: str, content_id: int, locale: str) -> Translation:
        data = self._http.get(f"/api/v2/help_center/{content_type}/{int(content_id)}/translations/{locale}")
        return to_domain(data=data["translation"], cls=Translation)

    def list_missing(self, content_type: str, content_id: int) -> list[str]:
        data = self._http.get(f"/api/v2/help_center/{content_type}/{int(content_id)}/translations/missing")
        return data.get("locales", [])

    def create(self, content_type: str, content_id: int, cmd: CreateTranslationCmd) -> Translation:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/help_center/{content_type}/{int(content_id)}/translations", json=payload)
        return to_domain(data=data["translation"], cls=Translation)

    def update(self, content_type: str, content_id: int, locale: str, cmd: UpdateTranslationCmd) -> Translation:
        payload = to_payload_update(cmd)
        data = self._http.put(
            f"/api/v2/help_center/{content_type}/{int(content_id)}/translations/{locale}", json=payload
        )
        return to_domain(data=data["translation"], cls=Translation)

    def delete(self, translation_id: int) -> None:
        self._http.delete(f"/api/v2/help_center/translations/{int(translation_id)}")
