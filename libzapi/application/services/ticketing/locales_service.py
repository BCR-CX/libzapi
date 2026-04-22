from __future__ import annotations

from typing import Iterable

from libzapi.domain.models.ticketing.locale import Locale
from libzapi.infrastructure.api_clients.ticketing.locale_api_client import (
    LocaleApiClient,
)


class LocalesService:
    def __init__(self, client: LocaleApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Locale]:
        return self._client.list_all()

    def list_agent(self) -> Iterable[Locale]:
        return self._client.list_agent()

    def list_public(self) -> Iterable[Locale]:
        return self._client.list_public()

    def get(self, locale_id_or_code: int | str) -> Locale:
        return self._client.get(locale_id_or_code=locale_id_or_code)

    def get_current(self) -> Locale:
        return self._client.get_current()

    def detect_best(self, available: Iterable[str]) -> Locale:
        return self._client.detect_best(available=available)
