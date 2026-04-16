from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.custom_data.object_trigger_cmds import (
    CreateObjectTriggerCmd,
    UpdateManyTriggersCmd,
    UpdateObjectTriggerCmd,
)
from libzapi.domain.models.custom_data.object_trigger import ObjectTrigger
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.custom_data.object_trigger_mapper import (
    to_payload_create,
    to_payload_update,
    to_payload_update_many,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


class ObjectTriggerApiClient:
    """HTTP adapter for Zendesk Object Triggers."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _triggers_path(self, key: str) -> str:
        return f"{_BASE}/{key}/triggers"

    def list_all(self, custom_object_key: str) -> Iterator[ObjectTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=self._triggers_path(custom_object_key),
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=ObjectTrigger)

    def list_active(self, custom_object_key: str) -> Iterator[ObjectTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{self._triggers_path(custom_object_key)}/active",
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=ObjectTrigger)

    def search(self, custom_object_key: str, query: str) -> Iterator[ObjectTrigger]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{self._triggers_path(custom_object_key)}/search?query={query}",
            base_url=self._http.base_url,
            items_key="triggers",
        ):
            yield to_domain(data=obj, cls=ObjectTrigger)

    def get(self, custom_object_key: str, trigger_id: int) -> ObjectTrigger:
        data = self._http.get(f"{self._triggers_path(custom_object_key)}/{int(trigger_id)}")
        return to_domain(data=data["trigger"], cls=ObjectTrigger)

    def definitions(self, custom_object_key: str) -> dict:
        return self._http.get(f"{self._triggers_path(custom_object_key)}/definitions")

    def create(self, custom_object_key: str, cmd: CreateObjectTriggerCmd) -> ObjectTrigger:
        payload = to_payload_create(cmd)
        data = self._http.post(self._triggers_path(custom_object_key), json=payload)
        return to_domain(data=data["trigger"], cls=ObjectTrigger)

    def update(self, custom_object_key: str, trigger_id: int, cmd: UpdateObjectTriggerCmd) -> ObjectTrigger:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{self._triggers_path(custom_object_key)}/{int(trigger_id)}", json=payload)
        return to_domain(data=data["trigger"], cls=ObjectTrigger)

    def update_many(self, custom_object_key: str, cmd: UpdateManyTriggersCmd) -> list[ObjectTrigger]:
        payload = to_payload_update_many(cmd)
        data = self._http.put(f"{self._triggers_path(custom_object_key)}/update_many", json=payload)
        return [to_domain(data=t, cls=ObjectTrigger) for t in data.get("triggers", [])]

    def delete(self, custom_object_key: str, trigger_id: int) -> None:
        self._http.delete(f"{self._triggers_path(custom_object_key)}/{int(trigger_id)}")

    def delete_many(self, custom_object_key: str, ids: list[int]) -> None:
        ids_str = ",".join(str(i) for i in ids)
        self._http.delete(f"{self._triggers_path(custom_object_key)}/destroy_many?ids={ids_str}")
