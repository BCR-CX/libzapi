from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.user_identity_cmds import (
    CreateUserIdentityCmd,
    UpdateUserIdentityCmd,
)
from libzapi.domain.models.ticketing.user_identity import UserIdentity
from libzapi.infrastructure.api_clients.ticketing.user_identity_api_client import (
    UserIdentityApiClient,
)


class UserIdentitiesService:
    """High-level service for Zendesk user identities."""

    def __init__(self, client: UserIdentityApiClient) -> None:
        self._client = client

    def list_for_user(self, user_id: int) -> Iterable[UserIdentity]:
        return self._client.list(user_id)

    def get_by_id(self, user_id: int, identity_id: int) -> UserIdentity:
        return self._client.get(user_id=user_id, identity_id=identity_id)

    def create(
        self,
        user_id: int,
        type: str,
        value: str,
        verified: bool | None = None,
        primary: bool | None = None,
    ) -> UserIdentity:
        return self._client.create(
            user_id=user_id,
            entity=CreateUserIdentityCmd(
                type=type, value=value, verified=verified, primary=primary
            ),
        )

    def update(
        self,
        user_id: int,
        identity_id: int,
        **fields,
    ) -> UserIdentity:
        return self._client.update(
            user_id=user_id,
            identity_id=identity_id,
            entity=UpdateUserIdentityCmd(**fields),
        )

    def delete(self, user_id: int, identity_id: int) -> None:
        self._client.delete(user_id=user_id, identity_id=identity_id)

    def make_primary(
        self, user_id: int, identity_id: int
    ) -> list[UserIdentity]:
        return self._client.make_primary(
            user_id=user_id, identity_id=identity_id
        )

    def verify(self, user_id: int, identity_id: int) -> UserIdentity:
        return self._client.verify(user_id=user_id, identity_id=identity_id)

    def request_verification(
        self, user_id: int, identity_id: int
    ) -> None:
        self._client.request_verification(
            user_id=user_id, identity_id=identity_id
        )
