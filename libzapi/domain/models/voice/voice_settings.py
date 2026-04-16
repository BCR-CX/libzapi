from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class VoiceSettings:
    voice: bool = False
    agent_confirmation_when_forwarding: bool = False
    agent_wrap_up_after_calls: bool = False
    maximum_queue_size: int = 0
    maximum_queue_wait_time: int = 0
    only_during_business_hours: bool = False
    recordings_public: bool = False
    voice_ai_enabled: bool = False
    voice_ai_display_transcript: bool = False
    voice_zendesk_qa_enabled: bool = False
    knowledge_suggestions_enabled: bool = False
    knowledge_suggestions_group_ids: list[int] = field(default_factory=list)
    voice_transcriptions_pii_redaction: bool = False
    voice_transcriptions_pci_redaction: bool = False
    voice_transcriptions_boosted_keywords_enabled: bool = False
    voice_transcriptions_boosted_keywords: str = ""
    supported_locales: list[str] = field(default_factory=list)
    voice_ai_enabled_lines: list[int] = field(default_factory=list)
    voice_zendesk_qa_enabled_lines: list[int] = field(default_factory=list)

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("voice_settings", "global")
