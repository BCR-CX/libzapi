from __future__ import annotations

from libzapi.application.commands.voice.voice_settings_cmds import UpdateVoiceSettingsCmd
from libzapi.domain.models.voice.voice_settings import VoiceSettings
from libzapi.infrastructure.api_clients.voice.voice_settings_api_client import VoiceSettingsApiClient


class VoiceSettingsService:
    def __init__(self, client: VoiceSettingsApiClient) -> None:
        self._client = client

    def get(self) -> VoiceSettings:
        return self._client.get()

    def update(self, **kwargs) -> VoiceSettings:
        cmd = UpdateVoiceSettingsCmd(**kwargs)
        return self._client.update(cmd=cmd)
