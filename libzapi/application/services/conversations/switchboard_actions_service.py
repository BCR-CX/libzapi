from __future__ import annotations

from libzapi.application.commands.conversations.switchboard_action_cmds import OfferControlCmd, PassControlCmd
from libzapi.infrastructure.api_clients.conversations.switchboard_action_api_client import SwitchboardActionApiClient


class SwitchboardActionsService:
    """High-level service for Sunshine Conversations Switchboard Actions."""

    def __init__(self, client: SwitchboardActionApiClient, app_id: str) -> None:
        self._client = client
        self._app_id = app_id

    def accept_control(self, conversation_id: str, metadata: dict | None = None):
        return self._client.accept_control(self._app_id, conversation_id, metadata=metadata)

    def offer_control(self, conversation_id: str, switchboard_integration: str, metadata: dict | None = None):
        cmd = OfferControlCmd(switchboardIntegration=switchboard_integration, metadata=metadata)
        return self._client.offer_control(self._app_id, conversation_id, cmd)

    def pass_control(self, conversation_id: str, switchboard_integration: str, metadata: dict | None = None):
        cmd = PassControlCmd(switchboardIntegration=switchboard_integration, metadata=metadata)
        return self._client.pass_control(self._app_id, conversation_id, cmd)

    def release_control(self, conversation_id: str, metadata: dict | None = None):
        return self._client.release_control(self._app_id, conversation_id, metadata=metadata)
