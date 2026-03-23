from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.domain.models.conversations.user import User
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.user_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class UserApiClient:
    """HTTP adapter for Sunshine Conversations Users."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_by_email(self, app_id: str, email: str) -> Iterator[User]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/users?filter[identities.email]={email}",
            items_key="users",
        ):
            yield to_domain(data=obj, cls=User)

    def get(self, app_id: str, user_id_or_external_id: str) -> User:
        data = self._http.get(f"/v2/apps/{app_id}/users/{user_id_or_external_id}")
        return to_domain(data=data["user"], cls=User)

    def create(self, app_id: str, cmd: CreateUserCmd) -> User:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/v2/apps/{app_id}/users", payload)
        return to_domain(data=data["user"], cls=User)

    def update(self, app_id: str, user_id_or_external_id: str, cmd: UpdateUserCmd) -> User:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"/v2/apps/{app_id}/users/{user_id_or_external_id}", payload)
        return to_domain(data=data["user"], cls=User)

    def delete(self, app_id: str, user_id_or_external_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/users/{user_id_or_external_id}")

    def delete_personal_info(self, app_id: str, user_id_or_external_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/users/{user_id_or_external_id}/personalinformation")

    def sync(self, app_id: str, zendesk_id: str) -> dict:
        return self._http.post(f"/v2/apps/{app_id}/users/{zendesk_id}/sync", {})
