from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.organization_membership_cmds import (
    CreateOrganizationMembershipCmd,
)
from libzapi.domain.models.ticketing.organization_membership import (
    OrganizationMembership,
)
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.organization_membership_mapper import (
    to_payload_create,
)
from libzapi.infrastructure.serialization.parse import to_domain


class OrganizationMembershipApiClient:
    """HTTP adapter for Zendesk Organization Memberships."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[OrganizationMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/organization_memberships",
            base_url=self._http.base_url,
            items_key="organization_memberships",
        ):
            yield to_domain(data=obj, cls=OrganizationMembership)

    def list_by_user(self, user_id: int) -> Iterator[OrganizationMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/organization_memberships",
            base_url=self._http.base_url,
            items_key="organization_memberships",
        ):
            yield to_domain(data=obj, cls=OrganizationMembership)

    def list_by_organization(
        self, organization_id: int
    ) -> Iterator[OrganizationMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/organizations/{int(organization_id)}/organization_memberships",
            base_url=self._http.base_url,
            items_key="organization_memberships",
        ):
            yield to_domain(data=obj, cls=OrganizationMembership)

    def get(self, membership_id: int) -> OrganizationMembership:
        data = self._http.get(
            f"/api/v2/organization_memberships/{int(membership_id)}"
        )
        return to_domain(
            data=data["organization_membership"], cls=OrganizationMembership
        )

    def get_for_user(
        self, user_id: int, membership_id: int
    ) -> OrganizationMembership:
        data = self._http.get(
            f"/api/v2/users/{int(user_id)}/organization_memberships/{int(membership_id)}"
        )
        return to_domain(
            data=data["organization_membership"], cls=OrganizationMembership
        )

    def create(
        self, entity: CreateOrganizationMembershipCmd
    ) -> OrganizationMembership:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/organization_memberships", payload)
        return to_domain(
            data=data["organization_membership"], cls=OrganizationMembership
        )

    def create_for_user(
        self, user_id: int, entity: CreateOrganizationMembershipCmd
    ) -> OrganizationMembership:
        payload = to_payload_create(entity)
        data = self._http.post(
            f"/api/v2/users/{int(user_id)}/organization_memberships", payload
        )
        return to_domain(
            data=data["organization_membership"], cls=OrganizationMembership
        )

    def delete(self, membership_id: int) -> None:
        self._http.delete(
            f"/api/v2/organization_memberships/{int(membership_id)}"
        )

    def delete_for_user(self, user_id: int, membership_id: int) -> None:
        self._http.delete(
            f"/api/v2/users/{int(user_id)}/organization_memberships/{int(membership_id)}"
        )

    def make_default(
        self, user_id: int, membership_id: int
    ) -> list[OrganizationMembership]:
        data = self._http.put(
            f"/api/v2/users/{int(user_id)}/organization_memberships/{int(membership_id)}/make_default",
            {},
        )
        return [
            to_domain(data=obj, cls=OrganizationMembership)
            for obj in data.get("results", []) or []
        ]

    def create_many(
        self, entities: Iterable[CreateOrganizationMembershipCmd]
    ) -> JobStatus:
        payload = {
            "organization_memberships": [
                to_payload_create(e)["organization_membership"] for e in entities
            ]
        }
        data = self._http.post(
            "/api/v2/organization_memberships/create_many", payload
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, membership_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in membership_ids)
        data = (
            self._http.delete(
                f"/api/v2/organization_memberships/destroy_many?ids={ids_str}"
            )
            or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
