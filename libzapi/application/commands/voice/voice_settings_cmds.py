from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UpdateVoiceSettingsCmd:
    agent_confirmation_when_forwarding: bool | None = None
    agent_wrap_up_after_calls: bool | None = None
    maximum_queue_size: int | None = None
    maximum_queue_wait_time: int | None = None
    only_during_business_hours: bool | None = None
    recordings_public: bool | None = None
