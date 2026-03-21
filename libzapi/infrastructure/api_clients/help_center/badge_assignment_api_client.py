from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.badge_assignment_cmds import CreateBadgeAssignmentCmd
from libzapi.domain.models.help_center.badge_assignment import BadgeAssignment
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.badge_assignment_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class BadgeAssignmentApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[BadgeAssignment]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/gather/badge_assignments",
            base_url=self._http.base_url,
            items_key="badge_assignments",
        ):
            yield to_domain(data=obj, cls=BadgeAssignment)

    def get(self, assignment_id: str) -> BadgeAssignment:
        data = self._http.get(f"/api/v2/gather/badge_assignments/{assignment_id}")
        return to_domain(data=data["badge_assignment"], cls=BadgeAssignment)

    def create(self, cmd: CreateBadgeAssignmentCmd) -> BadgeAssignment:
        payload = to_payload_create(cmd)
        data = self._http.post("/api/v2/gather/badge_assignments", json=payload)
        return to_domain(data=data["badge_assignment"], cls=BadgeAssignment)

    def delete(self, assignment_id: str) -> None:
        self._http.delete(f"/api/v2/gather/badge_assignments/{assignment_id}")
