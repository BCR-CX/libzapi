from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateCapacityRuleCmd:
    name: str
    capacities: dict
    description: str | None = None


@dataclass(frozen=True, slots=True)
class UpdateCapacityRuleCmd:
    name: str | None = None
    description: str | None = None
    capacities: dict | None = None
