from __future__ import annotations

from libzapi.application.commands.voice.voice_settings_cmds import UpdateVoiceSettingsCmd
from libzapi.domain.models.voice.voice_settings import VoiceSettings
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.voice_settings_mapper import to_payload_update
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/settings"


class VoiceSettingsApiClient:
    """HTTP adapter for Zendesk Voice Settings"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(self) -> VoiceSettings:
        data = self._http.get(_BASE)
        return to_domain(data=data["settings"], cls=VoiceSettings)

    def update(self, cmd: UpdateVoiceSettingsCmd) -> VoiceSettings:
        payload = to_payload_update(cmd)
        data = self._http.put(_BASE, json=payload)
        return to_domain(data=data["settings"], cls=VoiceSettings)
