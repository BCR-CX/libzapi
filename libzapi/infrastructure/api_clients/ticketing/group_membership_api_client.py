from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.group_membership_cmds import (
    CreateGroupMembershipCmd,
)
from libzapi.domain.models.ticketing.group_membership import GroupMembership
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.group_membership_mapper import (
    to_payload_create,
)
from libzapi.infrastructure.serialization.parse import to_domain


class GroupMembershipApiClient:
    """HTTP adapter for Zendesk Group Memberships."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[GroupMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/group_memberships",
            base_url=self._http.base_url,
            items_key="group_memberships",
        ):
            yield to_domain(data=obj, cls=GroupMembership)

    def list_by_user(self, user_id: int) -> Iterator[GroupMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/group_memberships",
            base_url=self._http.base_url,
            items_key="group_memberships",
        ):
            yield to_domain(data=obj, cls=GroupMembership)

    def list_by_group(self, group_id: int) -> Iterator[GroupMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/groups/{int(group_id)}/memberships",
            base_url=self._http.base_url,
            items_key="group_memberships",
        ):
            yield to_domain(data=obj, cls=GroupMembership)

    def list_assignable(self, group_id: int) -> Iterator[GroupMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/groups/{int(group_id)}/memberships/assignable",
            base_url=self._http.base_url,
            items_key="group_memberships",
        ):
            yield to_domain(data=obj, cls=GroupMembership)

    def list_assignable_for_user(self, user_id: int) -> Iterator[GroupMembership]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/group_memberships/assignable",
            base_url=self._http.base_url,
            items_key="group_memberships",
        ):
            yield to_domain(data=obj, cls=GroupMembership)

    def get(self, membership_id: int) -> GroupMembership:
        data = self._http.get(f"/api/v2/group_memberships/{int(membership_id)}")
        return to_domain(data=data["group_membership"], cls=GroupMembership)

    def get_for_user(self, user_id: int, membership_id: int) -> GroupMembership:
        data = self._http.get(
            f"/api/v2/users/{int(user_id)}/group_memberships/{int(membership_id)}"
        )
        return to_domain(data=data["group_membership"], cls=GroupMembership)

    def create(self, entity: CreateGroupMembershipCmd) -> GroupMembership:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/group_memberships", payload)
        return to_domain(data=data["group_membership"], cls=GroupMembership)

    def create_for_user(
        self, user_id: int, entity: CreateGroupMembershipCmd
    ) -> GroupMembership:
        payload = to_payload_create(entity)
        data = self._http.post(
            f"/api/v2/users/{int(user_id)}/group_memberships", payload
        )
        return to_domain(data=data["group_membership"], cls=GroupMembership)

    def delete(self, membership_id: int) -> None:
        self._http.delete(f"/api/v2/group_memberships/{int(membership_id)}")

    def delete_for_user(self, user_id: int, membership_id: int) -> None:
        self._http.delete(
            f"/api/v2/users/{int(user_id)}/group_memberships/{int(membership_id)}"
        )

    def make_default(self, user_id: int, membership_id: int) -> list[GroupMembership]:
        data = self._http.put(
            f"/api/v2/users/{int(user_id)}/group_memberships/{int(membership_id)}/make_default",
            {},
        )
        return [
            to_domain(data=obj, cls=GroupMembership)
            for obj in data.get("results", []) or []
        ]

    def create_many(
        self, entities: Iterable[CreateGroupMembershipCmd]
    ) -> JobStatus:
        payload = {
            "group_memberships": [to_payload_create(e)["group_membership"] for e in entities]
        }
        data = self._http.post("/api/v2/group_memberships/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, membership_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in membership_ids)
        data = (
            self._http.delete(
                f"/api/v2/group_memberships/destroy_many?ids={ids_str}"
            )
            or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)
