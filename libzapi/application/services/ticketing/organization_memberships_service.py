from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.organization_membership_cmds import (
    CreateOrganizationMembershipCmd,
)
from libzapi.domain.models.ticketing.organization_membership import (
    OrganizationMembership,
)
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.organization_membership_api_client import (
    OrganizationMembershipApiClient,
)


class OrganizationMembershipsService:
    """High-level service using the API client."""

    def __init__(self, client: OrganizationMembershipApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[OrganizationMembership]:
        return self._client.list()

    def list_by_user(self, user_id: int) -> Iterable[OrganizationMembership]:
        return self._client.list_by_user(user_id)

    def list_by_organization(
        self, organization_id: int
    ) -> Iterable[OrganizationMembership]:
        return self._client.list_by_organization(organization_id)

    def get_by_id(self, membership_id: int) -> OrganizationMembership:
        return self._client.get(membership_id)

    def get_for_user(
        self, user_id: int, membership_id: int
    ) -> OrganizationMembership:
        return self._client.get_for_user(user_id, membership_id)

    def create(
        self,
        user_id: int,
        organization_id: int,
        default: bool | None = None,
        view_tickets: bool | None = None,
    ) -> OrganizationMembership:
        return self._client.create(
            entity=CreateOrganizationMembershipCmd(
                user_id=user_id,
                organization_id=organization_id,
                default=default,
                view_tickets=view_tickets,
            )
        )

    def create_for_user(
        self,
        user_id: int,
        organization_id: int,
        default: bool | None = None,
        view_tickets: bool | None = None,
    ) -> OrganizationMembership:
        return self._client.create_for_user(
            user_id=user_id,
            entity=CreateOrganizationMembershipCmd(
                user_id=user_id,
                organization_id=organization_id,
                default=default,
                view_tickets=view_tickets,
            ),
        )

    def delete(self, membership_id: int) -> None:
        self._client.delete(membership_id)

    def delete_for_user(self, user_id: int, membership_id: int) -> None:
        self._client.delete_for_user(user_id, membership_id)

    def make_default(
        self, user_id: int, membership_id: int
    ) -> list[OrganizationMembership]:
        return self._client.make_default(user_id, membership_id)

    def create_many(self, memberships: Iterable[dict]) -> JobStatus:
        return self._client.create_many(
            entities=[CreateOrganizationMembershipCmd(**m) for m in memberships]
        )

    def destroy_many(self, membership_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(membership_ids=membership_ids)
