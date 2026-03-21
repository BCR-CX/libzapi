from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateContentSubscriptionCmd:
    locale: str = ""
