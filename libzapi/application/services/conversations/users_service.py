from __future__ import annotations

from libzapi.application.commands.conversations.user_cmds import CreateUserCmd, UpdateUserCmd
from libzapi.infrastructure.api_clients.conversations.user_api_client import UserApiClient


class UsersService:
    """High-level service for Sunshine Conversations Users."""

    def __init__(self, client: UserApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_by_email(self, email: str):
        return self._client.list_by_email(self._app_id, email)

    def get(self, user_id: str):
        return self._client.get(self._app_id, user_id)

    def create(self, external_id: str, **kwargs):
        cmd = CreateUserCmd(externalId=external_id, **kwargs)
        return self._client.create(self._app_id, cmd)

    def update(self, user_id: str, **kwargs):
        cmd = UpdateUserCmd(**kwargs)
        return self._client.update(self._app_id, user_id, cmd)

    def delete(self, user_id: str) -> None:
        self._client.delete(self._app_id, user_id)

    def delete_personal_info(self, user_id: str) -> None:
        self._client.delete_personal_info(self._app_id, user_id)

    def sync(self, zendesk_id: str):
        return self._client.sync(self._app_id, zendesk_id)
