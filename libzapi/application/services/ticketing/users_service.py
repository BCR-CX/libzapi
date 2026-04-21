from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.domain.models.ticketing.user import ComplianceDeletionStatus, User, UserRelated
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.user_api_client import UserApiClient


class UsersService:
    """High-level service using the API client."""

    def __init__(self, client: UserApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[User]:
        return self._client.list_all()

    def list_by_group(self, group_id: int) -> Iterable[User]:
        return self._client.list_by_group(group_id)

    def list_by_organization(self, organization_id: int) -> Iterable[User]:
        return self._client.list_by_organization(organization_id)

    def count(self) -> CountSnapshot:
        return self._client.count()

    def count_by_group(self, group_id: int) -> CountSnapshot:
        return self._client.count_by_group(group_id)

    def count_by_organization(self, organization_id: int) -> CountSnapshot:
        return self._client.count_by_organization(organization_id)

    def get_by_id(self, user_id: int) -> User:
        return self._client.get(user_id)

    def me(self) -> User:
        return self._client.me()

    def show_many(self, user_ids: Iterable[int]) -> Iterable[User]:
        return self._client.show_many(user_ids=user_ids)

    def search(self, query: str | None = None, external_id: str | None = None) -> Iterable[User]:
        return self._client.search(query=query, external_id=external_id)

    def autocomplete(self, name: str) -> Iterable[User]:
        return self._client.autocomplete(name=name)

    def list_related(self, user_id: int) -> UserRelated:
        return self._client.list_related(user_id=user_id)

    def list_compliance_deletion_statuses(
        self, user_id: int
    ) -> Iterable[ComplianceDeletionStatus]:
        return self._client.list_compliance_deletion_statuses(user_id=user_id)

    def list_deleted(self) -> Iterable[User]:
        return self._client.list_deleted()

    def count_deleted(self) -> CountSnapshot:
        return self._client.count_deleted()

    def show_deleted(self, deleted_user_id: int) -> User:
        return self._client.show_deleted(deleted_user_id=deleted_user_id)

    def me_settings(self) -> dict:
        return self._client.me_settings()

    def update_me_settings(self, settings: dict) -> dict:
        return self._client.update_me_settings(settings=settings)

    def list_entitlements(self, user_id: int) -> list[dict]:
        return self._client.list_entitlements(user_id=user_id)

    def create(self, **fields) -> User:
        return self._client.create(entity=CreateUserCmd(**fields))

    def update(self, user_id: int, **fields) -> User:
        return self._client.update(user_id=user_id, entity=UpdateUserCmd(**fields))

    def delete(self, user_id: int) -> User:
        return self._client.delete(user_id=user_id)

    def create_many(self, users: Iterable[dict]) -> JobStatus:
        return self._client.create_many(entities=[CreateUserCmd(**u) for u in users])

    def create_or_update(self, **fields) -> User:
        return self._client.create_or_update(entity=CreateUserCmd(**fields))

    def create_or_update_many(self, users: Iterable[dict]) -> JobStatus:
        return self._client.create_or_update_many(entities=[CreateUserCmd(**u) for u in users])

    def update_many(self, user_ids: Iterable[int], **fields) -> JobStatus:
        return self._client.update_many(user_ids=user_ids, entity=UpdateUserCmd(**fields))

    def update_many_individually(
        self, updates: Iterable[tuple[int, dict]]
    ) -> JobStatus:
        pairs = [(user_id, UpdateUserCmd(**fields)) for user_id, fields in updates]
        return self._client.update_many_individually(updates=pairs)

    def destroy_many(self, user_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(user_ids=user_ids)

    def merge(self, source_user_id: int, target_user_id: int) -> User:
        return self._client.merge(source_user_id=source_user_id, target_user_id=target_user_id)

    def permanently_delete(self, deleted_user_id: int) -> User:
        return self._client.permanently_delete(deleted_user_id=deleted_user_id)

    def request_create(self, **fields) -> dict:
        return self._client.request_create(entity=CreateUserCmd(**fields))

    def logout_many(self, user_ids: Iterable[int]) -> None:
        self._client.logout_many(user_ids=user_ids)

    def list_tags(self, user_id: int) -> list[str]:
        return self._client.list_tags(user_id=user_id)

    def set_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.set_tags(user_id=user_id, tags=tags)

    def add_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.add_tags(user_id=user_id, tags=tags)

    def remove_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.remove_tags(user_id=user_id, tags=tags)
