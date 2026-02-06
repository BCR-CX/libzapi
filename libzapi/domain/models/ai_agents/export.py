from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass(frozen=True, slots=True)
class ExportV3:
    date: date
    urls: list[str] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class TriggeredReplies:
    reply_timestamp: datetime
    reply_id: str
    reply_language: str
    reply_name: str
    reply_type: str
    intent_id: str


@dataclass(frozen=True, slots=True)
class TriggeredIntentReplies:
    intent_timestamp: datetime
    intent_id: str
    intent_name: str
    not_meaningful: bool


@dataclass(frozen=True, slots=True)
class Conversation:
    bot_id: str
    bot_name: str
    conversation_id: str
    platform_conversation_id: str
    conversation_start_time: datetime
    conversation_end_time: datetime
    conversation_type: str
    language: str
    channel: str
    labels: list[str]
    segments: list[str]
    conversations_data: str
    test_mode: bool
    conversation_status: str
    automated_resolution: str
    automated_resolution_reasoning: str
    last_resolution: str
    triggered_replies: list[TriggeredReplies]
    triggered_intent_replies: list[TriggeredIntentReplies]
    triggered_procedures: list[str]
    triggered_use_cases: list[str]
    has_knowledge_response_attempt: bool
    knowledge_notUndestood_count: int
    knowledge_responseGenerated_count: int
    knowledge_errorOccurred_count: int
    knowledge_escalationRequired_count: int
    knowledge_fallback_count: int
    knowledge_sources: str
    bot_messages_count: int
    visitor_messages_count: int
    not_understood_messages_count: int
