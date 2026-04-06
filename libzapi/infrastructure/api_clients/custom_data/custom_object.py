from typing import Iterator

from libzapi.application.commands.custom_data.custom_object_cmds import CreateCustomObjectCmd, UpdateCustomObjectCmd
from libzapi.domain.models.custom_data.custom_object import CustomObject
from libzapi.domain.shared_objects.custom_object_limit import CustomObjectLimit
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.custom_data.custom_object_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/custom_objects"


class CustomObjectApiClient:
    """HTTP adapter for Zendesk Custom Objects"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[CustomObject]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="custom_objects",
        ):
            yield to_domain(data=obj, cls=CustomObject)

    def get(self, custom_object_id: str) -> CustomObject:
        data = self._http.get(f"{_BASE}/{custom_object_id}")
        return to_domain(data=data["custom_object"], cls=CustomObject)

    def create(self, cmd: CreateCustomObjectCmd) -> CustomObject:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["custom_object"], cls=CustomObject)

    def update(self, custom_object_key: str, cmd: UpdateCustomObjectCmd) -> CustomObject:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"{_BASE}/{custom_object_key}", json=payload)
        return to_domain(data=data["custom_object"], cls=CustomObject)

    def delete(self, custom_object_key: str) -> None:
        self._http.delete(f"{_BASE}/{custom_object_key}")

    def limit(self) -> CustomObjectLimit:
        data = self._http.get(f"{_BASE}/limits/object_limit")
        return to_domain(data=data, cls=CustomObjectLimit)
