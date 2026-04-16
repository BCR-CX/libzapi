from typing import Iterator

from libzapi.application.commands.custom_data.custom_object_cmds import CreateCustomObjectCmd, UpdateCustomObjectCmd
from libzapi.domain.models.custom_data.custom_object import CustomObject
from libzapi.domain.shared_objects.custom_object_limit import CustomObjectLimit
from libzapi.infrastructure.api_clients.custom_data import CustomObjectApiClient


class CustomObjectsService:
    """High-level service using the API client."""

    def __init__(self, client: CustomObjectApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[CustomObject]:
        return self._client.list_all()

    def get(self, custom_object_id: str) -> CustomObject:
        return self._client.get(custom_object_id=custom_object_id)

    def create(self, key: str, title: str, title_pluralized: str, **kwargs) -> CustomObject:
        cmd = CreateCustomObjectCmd(key=key, title=title, title_pluralized=title_pluralized, **kwargs)
        return self._client.create(cmd=cmd)

    def update(self, custom_object_key: str, **kwargs) -> CustomObject:
        cmd = UpdateCustomObjectCmd(**kwargs)
        return self._client.update(custom_object_key=custom_object_key, cmd=cmd)

    def delete(self, custom_object_key: str) -> None:
        self._client.delete(custom_object_key=custom_object_key)

    def limit(self) -> CustomObjectLimit:
        return self._client.limit()
