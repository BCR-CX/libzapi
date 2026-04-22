from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.organization_field_cmds import (
    CreateOrganizationFieldCmd,
    OrganizationFieldOptionCmd,
    UpdateOrganizationFieldCmd,
)
from libzapi.domain.models.ticketing.organization_field import (
    OrganizationField,
    OrganizationFieldOption,
)
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.organization_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class OrganizationFieldApiClient:
    """HTTP adapter for Zendesk Organization Fields."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[OrganizationField]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/organization_fields",
            base_url=self._http.base_url,
            items_key="organization_fields",
        ):
            yield to_domain(data=obj, cls=OrganizationField)

    def get(self, organization_field_id: int) -> OrganizationField:
        data = self._http.get(
            f"/api/v2/organization_fields/{int(organization_field_id)}"
        )
        return to_domain(data=data["organization_field"], cls=OrganizationField)

    def create(self, entity: CreateOrganizationFieldCmd) -> OrganizationField:
        data = self._http.post(
            "/api/v2/organization_fields", to_payload_create(entity)
        )
        return to_domain(data=data["organization_field"], cls=OrganizationField)

    def update(
        self,
        organization_field_id: int,
        entity: UpdateOrganizationFieldCmd,
    ) -> OrganizationField:
        data = self._http.put(
            f"/api/v2/organization_fields/{int(organization_field_id)}",
            to_payload_update(entity),
        )
        return to_domain(data=data["organization_field"], cls=OrganizationField)

    def delete(self, organization_field_id: int) -> None:
        self._http.delete(
            f"/api/v2/organization_fields/{int(organization_field_id)}"
        )

    def reorder(self, organization_field_ids: Iterable[int]) -> None:
        payload = {"organization_field_ids": [int(i) for i in organization_field_ids]}
        self._http.put("/api/v2/organization_fields/reorder", payload)

    def list_options(
        self, organization_field_id: int
    ) -> Iterator[OrganizationFieldOption]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/organization_fields/{int(organization_field_id)}/options",
            base_url=self._http.base_url,
            items_key="custom_field_options",
        ):
            yield to_domain(data=obj, cls=OrganizationFieldOption)

    def get_option(
        self, organization_field_id: int, option_id: int
    ) -> OrganizationFieldOption:
        data = self._http.get(
            f"/api/v2/organization_fields/{int(organization_field_id)}/options/{int(option_id)}"
        )
        return to_domain(
            data=data["custom_field_option"], cls=OrganizationFieldOption
        )

    def upsert_option(
        self,
        organization_field_id: int,
        option: OrganizationFieldOptionCmd,
    ) -> OrganizationFieldOption:
        data = self._http.post(
            f"/api/v2/organization_fields/{int(organization_field_id)}/options",
            option_to_payload(option),
        )
        return to_domain(
            data=data["custom_field_option"], cls=OrganizationFieldOption
        )

    def delete_option(
        self, organization_field_id: int, option_id: int
    ) -> None:
        self._http.delete(
            f"/api/v2/organization_fields/{int(organization_field_id)}/options/{int(option_id)}"
        )
