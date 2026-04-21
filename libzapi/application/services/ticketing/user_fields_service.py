from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)
from libzapi.domain.models.ticketing.user_field import CustomFieldOption, UserField
from libzapi.infrastructure.api_clients.ticketing.user_field_api_client import (
    UserFieldApiClient,
)


class UserFieldsService:
    """High-level service using the API client."""

    def __init__(self, client: UserFieldApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[UserField]:
        return self._client.list_all()

    def list_options(self, user_field_id: int) -> Iterable[CustomFieldOption]:
        return self._client.list_options(user_field_id=user_field_id)

    def get_by_id(self, user_field_id: int) -> UserField:
        return self._client.get(user_field_id=user_field_id)

    def get_option_by_id(
        self, user_field_id: int, user_field_option_id: int
    ) -> CustomFieldOption:
        return self._client.get_option(
            user_field_id=user_field_id,
            user_field_option_id=user_field_option_id,
        )

    def create(self, **fields) -> UserField:
        return self._client.create(entity=CreateUserFieldCmd(**fields))

    def update(self, user_field_id: int, **fields) -> UserField:
        return self._client.update(
            user_field_id=user_field_id, entity=UpdateUserFieldCmd(**fields)
        )

    def delete(self, user_field_id: int) -> None:
        self._client.delete(user_field_id=user_field_id)

    def reorder(self, user_field_ids: Iterable[int]) -> None:
        self._client.reorder(user_field_ids=user_field_ids)

    def upsert_option(
        self,
        user_field_id: int,
        name: str,
        value: str,
        id: int | None = None,
    ) -> CustomFieldOption:
        return self._client.upsert_option(
            user_field_id=user_field_id,
            option=UserFieldOptionCmd(name=name, value=value, id=id),
        )

    def delete_option(
        self, user_field_id: int, user_field_option_id: int
    ) -> None:
        self._client.delete_option(
            user_field_id=user_field_id,
            user_field_option_id=user_field_option_id,
        )
