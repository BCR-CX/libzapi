from typing import Iterable
from libzapi.application.commands.help_center.badge_assignment_cmds import CreateBadgeAssignmentCmd
from libzapi.domain.models.help_center.badge_assignment import BadgeAssignment
from libzapi.infrastructure.api_clients.help_center.badge_assignment_api_client import BadgeAssignmentApiClient


class BadgeAssignmentsService:
    def __init__(self, client: BadgeAssignmentApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[BadgeAssignment]:
        return self._client.list_all()

    def get(self, assignment_id: str) -> BadgeAssignment:
        return self._client.get(assignment_id=assignment_id)

    def create(self, badge_id: str, user_id: int) -> BadgeAssignment:
        return self._client.create(cmd=CreateBadgeAssignmentCmd(badge_id=badge_id, user_id=user_id))

    def delete(self, assignment_id: str) -> None:
        self._client.delete(assignment_id=assignment_id)
