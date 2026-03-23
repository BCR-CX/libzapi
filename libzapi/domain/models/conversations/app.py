from __future__ import annotations

from dataclasses import dataclass, field

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class AppSettings:
    multiConvoEnabled: bool = False
    maskCreditCardNumbers: bool = False
    useAnimalNames: bool = False
    echoPostback: bool = False
    ignoreAutoConversationStart: bool = False
    conversationRetentionSeconds: int | None = None
    appLocalizationEnabled: bool = False


@dataclass(frozen=True, slots=True)
class App:
    id: str
    displayName: str = ""
    metadata: dict = field(default_factory=dict)
    settings: AppSettings | None = None

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("app", self.id)
