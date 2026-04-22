from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateOrganizationMembershipCmd:
    user_id: int
    organization_id: int
    default: bool | None = None
    view_tickets: bool | None = None
