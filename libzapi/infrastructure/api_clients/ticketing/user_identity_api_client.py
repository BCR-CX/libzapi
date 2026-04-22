from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)
from libzapi.domain.models.ticketing.user_identity import UserIdentity
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.user_identity_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class UserIdentityApiClient:
    """HTTP adapter for Zendesk User Identities."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self, user_id: int) -> Iterator[UserIdentity]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{int(user_id)}/identities",
            base_url=self._http.base_url,
            items_key="identities",
        ):
            yield to_domain(data=obj, cls=UserIdentity)

    def get(self, user_id: int, identity_id: int) -> UserIdentity:
        data = self._http.get(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}"
        )
        return to_domain(data=data["identity"], cls=UserIdentity)

    def create(
        self, user_id: int, entity: CreateUserIdentityCmd
    ) -> UserIdentity:
        payload = to_payload_create(entity)
        data = self._http.post(
            f"/api/v2/users/{int(user_id)}/identities", payload
        )
        return to_domain(data=data["identity"], cls=UserIdentity)

    def update(
        self,
        user_id: int,
        identity_id: int,
        entity: UpdateUserIdentityCmd,
    ) -> UserIdentity:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}",
            payload,
        )
        return to_domain(data=data["identity"], cls=UserIdentity)

    def delete(self, user_id: int, identity_id: int) -> None:
        self._http.delete(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}"
        )

    def make_primary(
        self, user_id: int, identity_id: int
    ) -> list[UserIdentity]:
        data = self._http.put(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}/make_primary",
            {},
        )
        return [
            to_domain(data=obj, cls=UserIdentity)
            for obj in data.get("identities", []) or []
        ]

    def verify(self, user_id: int, identity_id: int) -> UserIdentity:
        data = self._http.put(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}/verify",
            {},
        )
        return to_domain(data=data["identity"], cls=UserIdentity)

    def request_verification(
        self, user_id: int, identity_id: int
    ) -> None:
        self._http.put(
            f"/api/v2/users/{int(user_id)}/identities/{int(identity_id)}/request_verification",
            {},
        )
