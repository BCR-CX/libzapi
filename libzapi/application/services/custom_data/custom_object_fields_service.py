from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.custom_data.custom_object_field_cmds import (
    CreateCustomObjectFieldCmd,
    UpdateCustomObjectFieldCmd,
)
from libzapi.domain.models.custom_data.custom_object_field import CustomObjectField
from libzapi.infrastructure.api_clients.custom_data import CustomObjectFieldApiClient


class CustomObjectFieldsService:
    """High-level service using the API client."""

    def __init__(self, client: CustomObjectFieldApiClient) -> None:
        self._client = client

    def list_all(self, custom_object_key: str) -> Iterator[CustomObjectField]:
        return self._client.list_all(custom_object_key)

    def get(self, custom_object_key: str, custom_object_field_id: int) -> CustomObjectField:
        return self._client.get(custom_object_key=custom_object_key, custom_object_field_id=custom_object_field_id)

    def create(self, custom_object_key: str, type: str, key: str, title: str, **kwargs) -> CustomObjectField:
        cmd = CreateCustomObjectFieldCmd(type=type, key=key, title=title, **kwargs)
        return self._client.create(custom_object_key=custom_object_key, cmd=cmd)

    def update(self, custom_object_key: str, field_id: int, **kwargs) -> CustomObjectField:
        cmd = UpdateCustomObjectFieldCmd(**kwargs)
        return self._client.update(custom_object_key=custom_object_key, field_id=field_id, cmd=cmd)

    def delete(self, custom_object_key: str, field_id: int) -> None:
        self._client.delete(custom_object_key=custom_object_key, field_id=field_id)

    def reorder(self, custom_object_key: str, field_ids: list[int]) -> None:
        self._client.reorder(custom_object_key=custom_object_key, field_ids=field_ids)
