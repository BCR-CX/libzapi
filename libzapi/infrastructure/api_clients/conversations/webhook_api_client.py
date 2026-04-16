from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.conversations.webhook_cmds import CreateWebhookCmd, UpdateWebhookCmd
from libzapi.domain.models.conversations.webhook import Webhook
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.api_clients.conversations._pagination import sunco_yield_items
from libzapi.infrastructure.mappers.conversations.webhook_mapper import to_payload_create, to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain


class WebhookApiClient:
    """HTTP adapter for Sunshine Conversations Webhooks."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self, app_id: str, integration_id: str) -> Iterator[Webhook]:
        for obj in sunco_yield_items(
            http_client=self._http,
            first_path=f"/v2/apps/{app_id}/integrations/{integration_id}/webhooks",
            items_key="webhooks",
        ):
            yield to_domain(data=obj, cls=Webhook)

    def get(self, app_id: str, integration_id: str, webhook_id: str) -> Webhook:
        data = self._http.get(f"/v2/apps/{app_id}/integrations/{integration_id}/webhooks/{webhook_id}")
        return to_domain(data=data["webhook"], cls=Webhook)

    def create(self, app_id: str, integration_id: str, cmd: CreateWebhookCmd) -> Webhook:
        payload = to_payload_create(cmd)
        data = self._http.post(f"/v2/apps/{app_id}/integrations/{integration_id}/webhooks", payload)
        return to_domain(data=data["webhook"], cls=Webhook)

    def update(self, app_id: str, integration_id: str, webhook_id: str, cmd: UpdateWebhookCmd) -> Webhook:
        payload = to_payload_update(cmd)
        data = self._http.patch(
            f"/v2/apps/{app_id}/integrations/{integration_id}/webhooks/{webhook_id}",
            payload,
        )
        return to_domain(data=data["webhook"], cls=Webhook)

    def delete(self, app_id: str, integration_id: str, webhook_id: str) -> None:
        self._http.delete(f"/v2/apps/{app_id}/integrations/{integration_id}/webhooks/{webhook_id}")
