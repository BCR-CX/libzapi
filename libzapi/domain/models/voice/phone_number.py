from dataclasses import dataclass, field
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class PhoneNumber:
    id: int
    number: str = ""
    display_number: str = ""
    nickname: str = ""
    country_code: str = ""
    location: str = ""
    toll_free: bool = False
    external: bool = False
    voice_enabled: bool = False
    sms_enabled: bool = False
    outbound_enabled: bool = False
    recorded: bool = False
    transcription: bool = False
    priority: int = 0
    default_group_id: int | None = None
    group_ids: list[int] = field(default_factory=list)
    greeting_ids: list[int] = field(default_factory=list)
    schedule_id: int | None = None
    ivr_id: int | None = None
    capabilities: dict | None = None
    call_recording_consent: str = ""
    failover_number: str = ""
    token: str | None = None
    created_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("phone_number", str(self.id))


@dataclass(frozen=True, slots=True)
class AvailablePhoneNumber:
    number: str = ""
    display_number: str = ""
    toll_free: bool = False
    location: str = ""
    country_code: str = ""
    token: str = ""
    price: str = ""
    address_requirements: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("available_phone_number", self.number)
