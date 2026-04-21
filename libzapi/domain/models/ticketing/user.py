from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from libzapi.domain.shared_objects.logical_key import LogicalKey
from libzapi.domain.shared_objects.thumbnail import Thumbnail

OrganizationIdType = int | list[int] | None


@dataclass(frozen=True, slots=True)
class User:
    id: int
    url: str
    name: str
    email: Optional[str]
    created_at: datetime
    updated_at: datetime
    time_zone: str
    iana_time_zone: str
    phone: Optional[str]
    shared_phone_number: Optional[bool]
    photo: Optional[Thumbnail]
    locale_id: int
    locale: str
    organization_id: Optional[OrganizationIdType]
    role: str
    verified: bool
    external_id: Optional[str]
    tags: List[str]
    alias: Optional[str]
    active: bool
    shared: bool
    shared_agent: bool
    last_login_at: Optional[datetime]
    two_factor_auth_enabled: bool
    signature: Optional[str]
    details: Optional[str]
    notes: Optional[str]
    role_type: Optional[int]
    custom_role_id: Optional[int]
    is_billing_admin: bool
    moderator: bool
    ticket_restriction: Optional[str]
    only_private_comments: bool
    restricted_agent: bool
    suspended: bool
    default_group_id: Optional[int]
    report_csv: bool
    user_fields: Optional[dict] = None

    @property
    def logical_key(self) -> LogicalKey:
        base = f"id_{self.id}"
        return LogicalKey("user", base)


@dataclass(frozen=True, slots=True)
class UserRelated:
    assigned_tickets: int = 0
    requested_tickets: int = 0
    ccd_tickets: int = 0
    organization_subscriptions: int = 0
    topic_comments: int = 0
    topics: int = 0
    votes: int = 0
    subscriptions: int = 0


@dataclass(frozen=True, slots=True)
class ComplianceDeletionStatus:
    account_subdomain: Optional[str] = None
    action: Optional[str] = None
    application: Optional[str] = None
    created_at: Optional[datetime] = None
    executer_id: Optional[int] = None
    user_id: Optional[int] = None
