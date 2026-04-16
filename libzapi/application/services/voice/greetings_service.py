from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.greeting_cmds import CreateGreetingCmd, UpdateGreetingCmd
from libzapi.domain.models.voice.greeting import Greeting, GreetingCategory
from libzapi.infrastructure.api_clients.voice.greeting_api_client import GreetingApiClient


class GreetingsService:
    def __init__(self, client: GreetingApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[Greeting]:
        return self._client.list_all()

    def get(self, greeting_id: int) -> Greeting:
        return self._client.get(greeting_id=greeting_id)

    def create(self, category_id: int, name: str, audio_name: str = "") -> Greeting:
        cmd = CreateGreetingCmd(category_id=category_id, name=name, audio_name=audio_name)
        return self._client.create(cmd=cmd)

    def update(self, greeting_id: int, **kwargs) -> Greeting:
        cmd = UpdateGreetingCmd(**kwargs)
        return self._client.update(greeting_id=greeting_id, cmd=cmd)

    def delete(self, greeting_id: int) -> None:
        self._client.delete(greeting_id=greeting_id)

    def list_categories(self) -> Iterator[GreetingCategory]:
        return self._client.list_categories()

    def get_category(self, category_id: int) -> GreetingCategory:
        return self._client.get_category(category_id=category_id)
