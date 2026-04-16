from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AccountOverview:
    average_call_duration: int = 0
    average_queue_wait_time: int = 0
    average_wrap_up_time: int = 0
    max_calls_waiting: int = 0
    max_queue_wait_time: int = 0
    total_call_duration: int = 0
    total_calls: int = 0
    total_voicemails: int = 0
    total_wrap_up_time: int = 0
    average_callback_wait_time: int = 0
    average_hold_time: int = 0
    average_time_to_answer: int = 0
    total_callback_calls: int = 0
    total_calls_abandoned_in_queue: int = 0
    total_calls_outside_business_hours: int = 0
    total_calls_with_exceeded_queue_wait_time: int = 0
    total_calls_with_requested_voicemail: int = 0
    total_hold_time: int = 0
    total_inbound_calls: int = 0
    total_outbound_calls: int = 0
    total_textback_requests: int = 0
    total_embeddable_callback_calls: int = 0

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("account_overview", "current")


@dataclass(frozen=True, slots=True)
class AgentActivity:
    agent_id: int = 0
    name: str = ""
    agent_state: str = ""
    call_status: str | None = None
    via: str = ""
    avatar_url: str = ""
    forwarding_number: str = ""
    available_time: int = 0
    away_time: int = 0
    online_time: int = 0
    transfers_only_time: int = 0
    calls_accepted: int = 0
    calls_denied: int = 0
    calls_missed: int = 0
    total_call_duration: int = 0
    total_talk_time: int = 0
    total_wrap_up_time: int = 0

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("agent_activity", str(self.agent_id))


@dataclass(frozen=True, slots=True)
class AgentsOverview:
    average_wrap_up_time: int = 0
    total_calls_accepted: int = 0
    total_calls_denied: int = 0
    total_calls_missed: int = 0
    total_talk_time: int = 0
    total_wrap_up_time: int = 0

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("agents_overview", "current")


@dataclass(frozen=True, slots=True)
class CurrentQueueActivity:
    agents_online: int = 0
    average_wait_time: int = 0
    callbacks_waiting: int = 0
    calls_waiting: int = 0
    longest_wait_time: int = 0
    embeddable_callbacks_waiting: int = 0

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("current_queue_activity", "current")
