from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.greeting_cmds import (
    CreateGreetingCmd,
    UpdateGreetingCmd,
)
from libzapi.domain.models.voice.greeting import Greeting, GreetingCategory
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.voice.greeting_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/greetings"
_CATEGORIES_BASE = "/api/v2/channels/voice/greeting_categories"


class GreetingApiClient:
    """HTTP adapter for Zendesk Voice Greetings"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Greeting]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="greetings",
        ):
            yield to_domain(data=obj, cls=Greeting)

    def get(self, greeting_id: int) -> Greeting:
        data = self._http.get(f"{_BASE}/{int(greeting_id)}")
        return to_domain(data=data["greeting"], cls=Greeting)

    def create(self, cmd: CreateGreetingCmd) -> Greeting:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["greeting"], cls=Greeting)

    def update(self, greeting_id: int, cmd: UpdateGreetingCmd) -> Greeting:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{int(greeting_id)}", json=payload)
        return to_domain(data=data["greeting"], cls=Greeting)

    def delete(self, greeting_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(greeting_id)}")

    def list_categories(self) -> Iterator[GreetingCategory]:
        data = self._http.get(_CATEGORIES_BASE)
        for obj in data["greeting_categories"]:
            yield to_domain(data=obj, cls=GreetingCategory)

    def get_category(self, category_id: int) -> GreetingCategory:
        data = self._http.get(f"{_CATEGORIES_BASE}/{int(category_id)}")
        return to_domain(data=data["greeting_category"], cls=GreetingCategory)
