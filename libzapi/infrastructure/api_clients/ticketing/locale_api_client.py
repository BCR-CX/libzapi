from __future__ import annotations

from typing import Iterable, Iterator
from urllib.parse import urlencode

from libzapi.domain.models.ticketing.locale import Locale
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain


class LocaleApiClient:
    """HTTP adapter for Zendesk Locales."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Locale]:
        yield from self._list("/api/v2/locales")

    def list_agent(self) -> Iterator[Locale]:
        yield from self._list("/api/v2/locales/agent")

    def list_public(self) -> Iterator[Locale]:
        yield from self._list("/api/v2/locales/public")

    def get(self, locale_id_or_code: int | str) -> Locale:
        data = self._http.get(f"/api/v2/locales/{locale_id_or_code}")
        return to_domain(data=data["locale"], cls=Locale)

    def get_current(self) -> Locale:
        data = self._http.get("/api/v2/locales/current")
        return to_domain(data=data["locale"], cls=Locale)

    def detect_best(self, available: Iterable[str]) -> Locale:
        codes = ",".join(available)
        path = f"/api/v2/locales/detect_best_locale?{urlencode({'available': codes})}"
        data = self._http.get(path)
        return to_domain(data=data["locale"], cls=Locale)

    def _list(self, path: str) -> Iterator[Locale]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="locales",
        ):
            yield to_domain(data=obj, cls=Locale)
