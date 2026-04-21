from __future__ import annotations

from typing import Iterable, Iterator

from libzapi.application.commands.ticketing.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.domain.models.ticketing.user import ComplianceDeletionStatus, User, UserRelated
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.count_mapper import to_count_snapshot
from libzapi.infrastructure.mappers.ticketing.user_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class UserApiClient:
    """HTTP adapter for Zendesk Users with shared cursor pagination."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterable[User]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/users",
            base_url=self._http.base_url,
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def list_by_group(self, group_id) -> Iterable[User]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/groups/{group_id}/users",
            base_url=self._http.base_url,
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def list_by_organization(self, organization_id) -> Iterable[User]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/organizations/{organization_id}/users",
            base_url=self._http.base_url,
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def count(self) -> CountSnapshot:
        data = self._http.get("/api/v2/users/count")
        return to_count_snapshot(data["count"])

    def count_by_group(self, group_id) -> CountSnapshot:
        data = self._http.get(f"/api/v2/groups/{group_id}/users/count")
        return to_count_snapshot(data["count"])

    def count_by_organization(self, organization_id) -> CountSnapshot:
        data = self._http.get(f"/api/v2/organizations/{organization_id}/users/count")
        return to_count_snapshot(data["count"])

    def get(self, user_id: int) -> User:
        data = self._http.get(f"/api/v2/users/{int(user_id)}")
        return to_domain(data=data["user"], cls=User)

    def me(self) -> User:
        data = self._http.get("/api/v2/users/me")
        return to_domain(data=data["user"], cls=User)

    def show_many(self, user_ids: Iterable[int]) -> Iterator[User]:
        ids_str = ",".join(str(int(i)) for i in user_ids)
        data = self._http.get(f"/api/v2/users/show_many?ids={ids_str}")
        for obj in data["users"]:
            yield to_domain(data=obj, cls=User)

    def search(self, query: str | None = None, external_id: str | None = None) -> Iterator[User]:
        if external_id is not None:
            path = f"/api/v2/users/search?external_id={external_id}"
        else:
            path = f"/api/v2/users/search?query={query or ''}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def autocomplete(self, name: str) -> Iterator[User]:
        data = self._http.post("/api/v2/users/autocomplete", {"name": name})
        for obj in data.get("users", []):
            yield to_domain(data=obj, cls=User)

    def list_related(self, user_id: int) -> UserRelated:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/related")
        return to_domain(data=data["user_related"], cls=UserRelated)

    def list_compliance_deletion_statuses(
        self, user_id: int
    ) -> Iterator[ComplianceDeletionStatus]:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/compliance_deletion_statuses")
        for obj in data.get("compliance_deletion_statuses", []):
            yield to_domain(data=obj, cls=ComplianceDeletionStatus)

    def list_deleted(self) -> Iterator[User]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/deleted_users",
            base_url=self._http.base_url,
            items_key="deleted_users",
        ):
            yield to_domain(data=obj, cls=User)

    def count_deleted(self) -> CountSnapshot:
        data = self._http.get("/api/v2/deleted_users/count")
        return to_count_snapshot(data["count"])

    def show_deleted(self, deleted_user_id: int) -> User:
        data = self._http.get(f"/api/v2/deleted_users/{int(deleted_user_id)}")
        return to_domain(data=data["deleted_user"], cls=User)

    def me_settings(self) -> dict:
        data = self._http.get("/api/v2/users/me/settings")
        return data.get("settings", data)

    def update_me_settings(self, settings: dict) -> dict:
        data = self._http.put("/api/v2/users/me/settings", {"settings": settings})
        return data.get("settings", data)

    def list_entitlements(self, user_id: int) -> list[dict]:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/entitlements/full")
        return list(data.get("entitlements", []))

    def create(self, entity: CreateUserCmd) -> User:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/users", payload)
        return to_domain(data=data["user"], cls=User)

    def update(self, user_id: int, entity: UpdateUserCmd) -> User:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/users/{int(user_id)}", payload)
        return to_domain(data=data["user"], cls=User)

    def delete(self, user_id: int) -> User:
        data = self._http.delete(f"/api/v2/users/{int(user_id)}") or {}
        return to_domain(data=data["user"], cls=User)

    def create_many(self, entities: Iterable[CreateUserCmd]) -> JobStatus:
        payload = {"users": [to_payload_create(e)["user"] for e in entities]}
        data = self._http.post("/api/v2/users/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def create_or_update(self, entity: CreateUserCmd) -> User:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/users/create_or_update", payload)
        return to_domain(data=data["user"], cls=User)

    def create_or_update_many(self, entities: Iterable[CreateUserCmd]) -> JobStatus:
        payload = {"users": [to_payload_create(e)["user"] for e in entities]}
        data = self._http.post("/api/v2/users/create_or_update_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many(self, user_ids: Iterable[int], entity: UpdateUserCmd) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in user_ids)
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/users/update_many?ids={ids_str}", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many_individually(
        self, updates: Iterable[tuple[int, UpdateUserCmd]]
    ) -> JobStatus:
        users = []
        for user_id, cmd in updates:
            user_payload = to_payload_update(cmd)["user"]
            user_payload["id"] = int(user_id)
            users.append(user_payload)
        data = self._http.put("/api/v2/users/update_many", {"users": users})
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, user_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in user_ids)
        data = self._http.delete(f"/api/v2/users/destroy_many?ids={ids_str}") or {}
        return to_domain(data=data["job_status"], cls=JobStatus)

    def merge(self, source_user_id: int, target_user_id: int) -> User:
        data = self._http.put(
            f"/api/v2/users/{int(source_user_id)}/merge",
            {"user": {"id": int(target_user_id)}},
        )
        return to_domain(data=data["user"], cls=User)

    def permanently_delete(self, deleted_user_id: int) -> User:
        data = self._http.delete(f"/api/v2/deleted_users/{int(deleted_user_id)}") or {}
        return to_domain(data=data["deleted_user"], cls=User)

    def request_create(self, entity: CreateUserCmd) -> dict:
        payload = to_payload_create(entity)
        return self._http.post("/api/v2/users/request_create", payload)

    def logout_many(self, user_ids: Iterable[int]) -> None:
        ids_str = ",".join(str(int(i)) for i in user_ids)
        self._http.post(f"/api/v2/users/logout_many?ids={ids_str}", {})

    def list_tags(self, user_id: int) -> list[str]:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/tags")
        return list(data.get("tags", []))

    def set_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.post(f"/api/v2/users/{int(user_id)}/tags", {"tags": list(tags)})
        return list(data.get("tags", []))

    def add_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.put(f"/api/v2/users/{int(user_id)}/tags", {"tags": list(tags)})
        return list(data.get("tags", []))

    def remove_tags(self, user_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.delete(
            f"/api/v2/users/{int(user_id)}/tags", json={"tags": list(tags)}
        )
        return list((data or {}).get("tags", []))
