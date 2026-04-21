from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)
from libzapi.domain.models.ticketing.organization import Organization, OrganizationRelated
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.organization_api_client import (
    OrganizationApiClient,
)


class OrganizationsService:
    """High-level service using the API client."""

    def __init__(self, client: OrganizationApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[Organization]:
        return self._client.list()

    def list_by_user(self, user_id: int) -> Iterable[Organization]:
        return self._client.list_organizations(user_id)

    def count(self) -> CountSnapshot:
        return self._client.count()

    def get_by_id(self, organization_id: int) -> Organization:
        return self._client.get(organization_id)

    def show_many(
        self,
        organization_ids: Iterable[int] | None = None,
        external_ids: Iterable[str] | None = None,
    ) -> Iterable[Organization]:
        return self._client.show_many(
            organization_ids=organization_ids, external_ids=external_ids
        )

    def search(
        self, external_id: str | None = None, name: str | None = None
    ) -> Iterable[Organization]:
        return self._client.search(external_id=external_id, name=name)

    def autocomplete(self, name: str) -> Iterable[Organization]:
        return self._client.autocomplete(name=name)

    def list_related(self, organization_id: int) -> OrganizationRelated:
        return self._client.list_related(organization_id=organization_id)

    def create(self, **fields) -> Organization:
        return self._client.create(entity=CreateOrganizationCmd(**fields))

    def update(self, organization_id: int, **fields) -> Organization:
        return self._client.update(
            organization_id=organization_id, entity=UpdateOrganizationCmd(**fields)
        )

    def delete(self, organization_id: int) -> None:
        self._client.delete(organization_id=organization_id)

    def create_many(self, organizations: Iterable[dict]) -> JobStatus:
        return self._client.create_many(
            entities=[CreateOrganizationCmd(**o) for o in organizations]
        )

    def create_or_update(self, **fields) -> Organization:
        return self._client.create_or_update(entity=CreateOrganizationCmd(**fields))

    def update_many(self, organization_ids: Iterable[int], **fields) -> JobStatus:
        return self._client.update_many(
            organization_ids=organization_ids, entity=UpdateOrganizationCmd(**fields)
        )

    def update_many_individually(
        self, updates: Iterable[tuple[int, dict]]
    ) -> JobStatus:
        pairs = [
            (organization_id, UpdateOrganizationCmd(**fields))
            for organization_id, fields in updates
        ]
        return self._client.update_many_individually(updates=pairs)

    def destroy_many(self, organization_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(organization_ids=organization_ids)

    def list_tags(self, organization_id: int) -> list[str]:
        return self._client.list_tags(organization_id=organization_id)

    def set_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.set_tags(organization_id=organization_id, tags=tags)

    def add_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.add_tags(organization_id=organization_id, tags=tags)

    def remove_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.remove_tags(organization_id=organization_id, tags=tags)
