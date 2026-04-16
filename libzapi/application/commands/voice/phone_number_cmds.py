from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreatePhoneNumberCmd:
    token: str
    nickname: str = ""
    address_sid: str | None = None


@dataclass(frozen=True, slots=True)
class UpdatePhoneNumberCmd:
    nickname: str | None = None
    default_group_id: int | None = None
    group_ids: list[int] | None = None
    priority: int | None = None
    outbound_enabled: bool | None = None
    voice_enabled: bool | None = None
    sms_enabled: bool | None = None
    recorded: bool | None = None
    transcription: bool | None = None
    greeting_ids: list[int] | None = None
    schedule_id: int | None = None
    ivr_id: int | None = None
    call_recording_consent: str | None = None
    failover_number: str | None = None
