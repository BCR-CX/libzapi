from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Engagement:
    engagement_id: str
    agent_id: str | None = None
    group_id: str | None = None
    ticket_id: str | None = None
    requester_id: int | None = None
    channel: str | None = None
    engagement_start_time: str | None = None
    engagement_end_time: str | None = None
    engagement_start_reason: str | None = None
    engagement_end_reason: str | None = None
    ticket_status_start: str | None = None
    ticket_status_end: str | None = None
    agent_messages_count: int | None = None
    agent_replies_count: int | None = None
    end_user_messages_count: int | None = None
    assignment_to_first_reply_time_seconds: int | None = None
    offer_time_seconds: int | None = None
    average_requester_wait_time_seconds: int | None = None
    longest_requester_wait_time_seconds: int | None = None
    total_requester_wait_time_seconds: int | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("engagement", self.engagement_id)
