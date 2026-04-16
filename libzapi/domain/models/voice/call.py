from dataclasses import dataclass, field
from datetime import datetime

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Call:
    id: int
    agent_id: int | None = None
    direction: str = ""
    duration: int = 0
    talk_time: int = 0
    hold_time: int = 0
    wait_time: int = 0
    wrap_up_time: int = 0
    time_to_answer: int = 0
    phone_number: str = ""
    phone_number_id: int | None = None
    ticket_id: int | None = None
    voicemail: bool = False
    callback: bool = False
    callback_source: str = ""
    completion_status: str = ""
    call_charge: str = ""
    minutes_billed: int = 0
    recording_time: int = 0
    outside_business_hours: bool = False
    exceeded_queue_time: bool = False
    overflowed: bool = False
    overflowed_to: str = ""
    call_channel: str = ""
    line_type: str = ""
    ivr_action: str = ""
    ivr_hops: int = 0
    ivr_routed_to: str = ""
    ivr_time_spent: int = 0
    quality_issues: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("call", str(self.id))


@dataclass(frozen=True, slots=True)
class CallLeg:
    id: int
    call_id: int = 0
    agent_id: int | None = None
    user_id: int | None = None
    type: str = ""
    duration: int = 0
    talk_time: int = 0
    hold_time: int = 0
    wrap_up_time: int = 0
    minutes_billed: int = 0
    call_charge: str = ""
    completion_status: str = ""
    available_via: str = ""
    forwarded_to: str = ""
    transferred_from: int | None = None
    transferred_to: int | None = None
    conference_from: int | None = None
    conference_to: int | None = None
    conference_time: int = 0
    consultation_from: int | None = None
    consultation_to: int | None = None
    consultation_time: int = 0
    quality_issues: list[str] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("call_leg", str(self.id))
