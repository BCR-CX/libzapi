from typing import Iterator

from libzapi.application.commands.custom_data.custom_object_field_cmds import (
    CreateCustomObjectFieldCmd,
    UpdateCustomObjectFieldCmd,
)
from libzapi.domain.models.custom_data.custom_object_field import CustomObjectField
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.custom_data.custom_object_field_mapper import (
    to_payload_create,
    to_payload_reorder,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class CustomObjectFieldApiClient:
    """HTTP adapter for Zendesk Custom Objects Fields"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, custom_object_key: str) -> Iterator[CustomObjectField]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/custom_objects/{custom_object_key}/fields",
            base_url=self._http.base_url,
            items_key="custom_object_fields",
        ):
            yield to_domain(data=obj, cls=CustomObjectField)

    def get(self, custom_object_key: str, custom_object_field_id: int) -> CustomObjectField:
        data = self._http.get(f"/api/v2/custom_objects/{custom_object_key}/fields/{custom_object_field_id}")
        return to_domain(data=data["custom_object_field"], cls=CustomObjectField)

    def create(self, custom_object_key: str, cmd: CreateCustomObjectFieldCmd) -> CustomObjectField:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/api/v2/custom_objects/{custom_object_key}/fields", json=payload)
        return to_domain(data=data["custom_object_field"], cls=CustomObjectField)

    def update(self, custom_object_key: str, field_id: int, cmd: UpdateCustomObjectFieldCmd) -> CustomObjectField:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"/api/v2/custom_objects/{custom_object_key}/fields/{field_id}", json=payload)
        return to_domain(data=data["custom_object_field"], cls=CustomObjectField)

    def delete(self, custom_object_key: str, field_id: int) -> None:
        self._http.delete(f"/api/v2/custom_objects/{custom_object_key}/fields/{field_id}")

    def reorder(self, custom_object_key: str, field_ids: list[int]) -> None:
        payload = to_payload_reorder(field_ids)
        self._http.put(f"/api/v2/custom_objects/{custom_object_key}/fields/reorder", json=payload)
