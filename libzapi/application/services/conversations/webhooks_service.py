from __future__ import annotations

from libzapi.application.commands.conversations.webhook_cmds import CreateWebhookCmd, UpdateWebhookCmd
from libzapi.infrastructure.api_clients.conversations.webhook_api_client import WebhookApiClient


class WebhooksService:
    """High-level service for Sunshine Conversations Webhooks."""

    def __init__(self, client: WebhookApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def list_all(self, integration_id: str):
        return self._client.list_all(self._app_id, integration_id)

    def get(self, integration_id: str, webhook_id: str):
        return self._client.get(self._app_id, integration_id, webhook_id)

    def create(self, integration_id: str, target: str, triggers: list[str], **kwargs):
        cmd = CreateWebhookCmd(target=target, triggers=triggers, **kwargs)
        return self._client.create(self._app_id, integration_id, cmd)

    def update(self, integration_id: str, webhook_id: str, **kwargs):
        cmd = UpdateWebhookCmd(**kwargs)
        return self._client.update(self._app_id, integration_id, webhook_id, cmd)

    def delete(self, integration_id: str, webhook_id: str) -> None:
        self._client.delete(self._app_id, integration_id, webhook_id)
