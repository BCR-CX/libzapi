from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.group_membership_cmds import (
    CreateGroupMembershipCmd,
)
from libzapi.domain.models.ticketing.group_membership import GroupMembership
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.group_membership_api_client import (
    GroupMembershipApiClient,
)


class GroupMembershipsService:
    """High-level service using the API client."""

    def __init__(self, client: GroupMembershipApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[GroupMembership]:
        return self._client.list()

    def list_by_user(self, user_id: int) -> Iterable[GroupMembership]:
        return self._client.list_by_user(user_id)

    def list_by_group(self, group_id: int) -> Iterable[GroupMembership]:
        return self._client.list_by_group(group_id)

    def list_assignable(self, group_id: int) -> Iterable[GroupMembership]:
        return self._client.list_assignable(group_id)

    def list_assignable_for_user(self, user_id: int) -> Iterable[GroupMembership]:
        return self._client.list_assignable_for_user(user_id)

    def get_by_id(self, membership_id: int) -> GroupMembership:
        return self._client.get(membership_id)

    def get_for_user(self, user_id: int, membership_id: int) -> GroupMembership:
        return self._client.get_for_user(user_id, membership_id)

    def create(self, user_id: int, group_id: int, default: bool | None = None) -> GroupMembership:
        return self._client.create(
            entity=CreateGroupMembershipCmd(
                user_id=user_id, group_id=group_id, default=default
            )
        )

    def create_for_user(
        self, user_id: int, group_id: int, default: bool | None = None
    ) -> GroupMembership:
        return self._client.create_for_user(
            user_id=user_id,
            entity=CreateGroupMembershipCmd(
                user_id=user_id, group_id=group_id, default=default
            ),
        )

    def delete(self, membership_id: int) -> None:
        self._client.delete(membership_id)

    def delete_for_user(self, user_id: int, membership_id: int) -> None:
        self._client.delete_for_user(user_id, membership_id)

    def make_default(self, user_id: int, membership_id: int) -> list[GroupMembership]:
        return self._client.make_default(user_id, membership_id)

    def create_many(self, memberships: Iterable[dict]) -> JobStatus:
        return self._client.create_many(
            entities=[CreateGroupMembershipCmd(**m) for m in memberships]
        )

    def destroy_many(self, membership_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(membership_ids=membership_ids)
