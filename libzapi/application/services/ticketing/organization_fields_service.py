from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.organization_field_cmds import (
    CreateOrganizationFieldCmd,
    OrganizationFieldOptionCmd,
    UpdateOrganizationFieldCmd,
)
from libzapi.domain.models.ticketing.organization_field import (
    OrganizationField,
    OrganizationFieldOption,
)
from libzapi.infrastructure.api_clients.ticketing.organization_field_api_client import (
    OrganizationFieldApiClient,
)


class OrganizationFieldsService:
    def __init__(self, client: OrganizationFieldApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[OrganizationField]:
        return self._client.list_all()

    def get_by_id(self, organization_field_id: int) -> OrganizationField:
        return self._client.get(organization_field_id=organization_field_id)

    def create(self, **fields) -> OrganizationField:
        return self._client.create(entity=CreateOrganizationFieldCmd(**fields))

    def update(
        self, organization_field_id: int, **fields
    ) -> OrganizationField:
        return self._client.update(
            organization_field_id=organization_field_id,
            entity=UpdateOrganizationFieldCmd(**fields),
        )

    def delete(self, organization_field_id: int) -> None:
        self._client.delete(organization_field_id=organization_field_id)

    def reorder(self, organization_field_ids: Iterable[int]) -> None:
        self._client.reorder(organization_field_ids=organization_field_ids)

    def list_options(
        self, organization_field_id: int
    ) -> Iterable[OrganizationFieldOption]:
        return self._client.list_options(
            organization_field_id=organization_field_id
        )

    def get_option_by_id(
        self, organization_field_id: int, option_id: int
    ) -> OrganizationFieldOption:
        return self._client.get_option(
            organization_field_id=organization_field_id, option_id=option_id
        )

    def upsert_option(
        self,
        organization_field_id: int,
        name: str,
        value: str,
        id: int | None = None,
    ) -> OrganizationFieldOption:
        return self._client.upsert_option(
            organization_field_id=organization_field_id,
            option=OrganizationFieldOptionCmd(name=name, value=value, id=id),
        )

    def delete_option(
        self, organization_field_id: int, option_id: int
    ) -> None:
        self._client.delete_option(
            organization_field_id=organization_field_id, option_id=option_id
        )
