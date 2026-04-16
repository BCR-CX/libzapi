from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.custom_data.object_trigger_cmds import (
    CreateObjectTriggerCmd,
    UpdateManyTriggersCmd,
    UpdateObjectTriggerCmd,
)
from libzapi.domain.models.custom_data.object_trigger import ObjectTrigger
from libzapi.infrastructure.api_clients.custom_data import ObjectTriggerApiClient


class ObjectTriggersService:
    def __init__(self, client: ObjectTriggerApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str) -> Iterator[ObjectTrigger]:
        return self._client.list_all(custom_object_key=custom_object_key)

    def list_active(self, custom_object_key: str) -> Iterator[ObjectTrigger]:
        return self._client.list_active(custom_object_key=custom_object_key)

    def search(self, custom_object_key: str, query: str) -> Iterator[ObjectTrigger]:
        return self._client.search(custom_object_key=custom_object_key, query=query)

    def get(self, custom_object_key: str, trigger_id: int) -> ObjectTrigger:
        return self._client.get(custom_object_key=custom_object_key, trigger_id=trigger_id)

    def definitions(self, custom_object_key: str) -> dict:
        return self._client.definitions(custom_object_key=custom_object_key)

    def create(
        self, custom_object_key: str, title: str, conditions: dict, actions: list[dict], **kwargs
    ) -> ObjectTrigger:
        cmd = CreateObjectTriggerCmd(title=title, conditions=conditions, actions=actions, **kwargs)
        return self._client.create(custom_object_key=custom_object_key, cmd=cmd)

    def update(self, custom_object_key: str, trigger_id: int, **kwargs) -> ObjectTrigger:
        cmd = UpdateObjectTriggerCmd(**kwargs)
        return self._client.update(custom_object_key=custom_object_key, trigger_id=trigger_id, cmd=cmd)

    def update_many(self, custom_object_key: str, triggers: list[dict]) -> list[ObjectTrigger]:
        cmd = UpdateManyTriggersCmd(triggers=triggers)
        return self._client.update_many(custom_object_key=custom_object_key, cmd=cmd)

    def delete(self, custom_object_key: str, trigger_id: int) -> None:
        self._client.delete(custom_object_key=custom_object_key, trigger_id=trigger_id)

    def delete_many(self, custom_object_key: str, ids: list[int]) -> None:
        self._client.delete_many(custom_object_key=custom_object_key, ids=ids)
