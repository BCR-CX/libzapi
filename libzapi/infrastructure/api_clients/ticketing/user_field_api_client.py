from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)
from libzapi.domain.models.ticketing.user_field import CustomFieldOption, UserField
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.user_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class UserFieldApiClient:
    """HTTP adapter for Zendesk User Fields with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[UserField]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/user_fields",
            base_url=self._http.base_url,
            items_key="user_fields",
        ):
            yield to_domain(data=obj, cls=UserField)

    def list_options(self, user_field_id: int) -> Iterator[CustomFieldOption]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/user_fields/{int(user_field_id)}/options",
            base_url=self._http.base_url,
            items_key="custom_field_options",
        ):
            yield to_domain(data=obj, cls=CustomFieldOption)

    def get(self, user_field_id: int) -> UserField:
        data = self._http.get(f"/api/v2/user_fields/{int(user_field_id)}")
        return to_domain(data=data["user_field"], cls=UserField)

    def get_option(
        self, user_field_id: int, user_field_option_id: int
    ) -> CustomFieldOption:
        data = self._http.get(
            f"/api/v2/user_fields/{int(user_field_id)}/options/{int(user_field_option_id)}"
        )
        return to_domain(data=data["custom_field_option"], cls=CustomFieldOption)

    def create(self, entity: CreateUserFieldCmd) -> UserField:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/user_fields", payload)
        return to_domain(data=data["user_field"], cls=UserField)

    def update(self, user_field_id: int, entity: UpdateUserFieldCmd) -> UserField:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/user_fields/{int(user_field_id)}", payload
        )
        return to_domain(data=data["user_field"], cls=UserField)

    def delete(self, user_field_id: int) -> None:
        self._http.delete(f"/api/v2/user_fields/{int(user_field_id)}")

    def reorder(self, user_field_ids: Iterable[int]) -> None:
        payload = {"user_field_ids": [int(i) for i in user_field_ids]}
        self._http.put("/api/v2/user_fields/reorder", payload)

    def upsert_option(
        self, user_field_id: int, option: UserFieldOptionCmd
    ) -> CustomFieldOption:
        payload = option_to_payload(option)
        data = self._http.post(
            f"/api/v2/user_fields/{int(user_field_id)}/options", payload
        )
        return to_domain(data=data["custom_field_option"], cls=CustomFieldOption)

    def delete_option(
        self, user_field_id: int, user_field_option_id: int
    ) -> None:
        self._http.delete(
            f"/api/v2/user_fields/{int(user_field_id)}/options/{int(user_field_option_id)}"
        )
