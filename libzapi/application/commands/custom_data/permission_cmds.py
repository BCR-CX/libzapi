from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class UpdatePermissionPolicyCmd:
    create: str | None = None
    read: str | None = None
    update: str | None = None
    delete: str | None = None
    create_rule_id: str | None = None
    read_rule_id: str | None = None
    update_rule_id: str | None = None
    delete_rule_id: str | None = None


@dataclass(frozen=True, slots=True)
class CreateAccessRuleCmd:
    name: str
    conditions: dict = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class UpdateAccessRuleCmd:
    name: str | None = None
    conditions: dict | None = None
