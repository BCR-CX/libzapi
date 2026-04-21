from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.ticket_cmds import (
    CreateTicketCmd,
    MergeTicketsCmd,
    TicketCmd,
    UpdateTicketCmd,
)
from libzapi.domain.models.ticketing.ticket import (
    CustomField,
    ProblemMatch,
    Ticket,
    TicketRelated,
    User,
)
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing.ticket_api_client import TicketApiClient


class TickestService:
    """High-level service using the API client."""

    def __init__(self, client: TicketApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[Ticket]:
        return self._client.list()

    def list_organization(self, organization_id: int) -> Iterable[Ticket]:
        return self._client.list_organization(organization_id=organization_id)

    def list_user_requested(self, user_id: int) -> Iterable[Ticket]:
        return self._client.list_user_requested(user_id=user_id)

    def list_user_ccd(self, user_id: int) -> Iterable[Ticket]:
        return self._client.list_user_ccd(user_id=user_id)

    def list_user_followed(self, user_id: int) -> Iterable[Ticket]:
        return self._client.list_user_followed(user_id=user_id)

    def list_user_assigned(self, user_id: int) -> Iterable[Ticket]:
        return self._client.list_user_assigned(user_id=user_id)

    def list_recent(self) -> Iterable[Ticket]:
        return self._client.list_recent()

    def list_collaborators(self, ticket_id: int) -> Iterable[User]:
        return self._client.list_collaborators(ticket_id=ticket_id)

    def list_followers(self, ticket_id: int) -> Iterable[User]:
        return self._client.list_followers(ticket_id=ticket_id)

    def list_email_ccs(self, ticket_id: int) -> Iterable[User]:
        return self._client.list_email_ccs(ticket_id=ticket_id)

    def list_incidents(self, ticket_id: int) -> Iterable[Ticket]:
        return self._client.list_incidents(ticket_id=ticket_id)

    def list_problems(self) -> Iterable[Ticket]:
        return self._client.list_problems()

    def get(self, ticket_id: int) -> Ticket:
        return self._client.get(ticket_id=ticket_id)

    def count(self) -> CountSnapshot:
        return self._client.count()

    def organization_count(self, organization_id: int) -> CountSnapshot:
        return self._client.organization_count(organization_id=organization_id)

    def user_ccd_count(self, user_id: int) -> CountSnapshot:
        return self._client.user_ccd_count(user_id=user_id)

    def user_assigned_count(self, user_id: int) -> CountSnapshot:
        return self._client.user_assigned_count(user_id=user_id)

    def create(
        self,
        subject: str,
        description: str,
        tags: Iterable[str] = (),
        custom_fields: Iterable[dict] = (),
        priority: str = "",
        ticket_type: str = "",
        group_id: int = None,
        requester_id: int = None,
        organization_id: int = None,
        problem_id: int = None,
        ticket_form_id: int = None,
        brand_id: int = None,
    ) -> Ticket:
        fields = []
        for custom_field in custom_fields:
            field = CustomField(id=custom_field["id"], value=custom_field["value"])
            fields.append(field)

        entity = self.cast_to_ticket_command(
            CreateTicketCmd,
            brand_id,
            description,
            fields,
            group_id,
            organization_id,
            priority,
            problem_id,
            requester_id,
            subject,
            tags,
            ticket_form_id,
            ticket_type,
        )
        return self._client.create_ticket(entity=entity)

    @staticmethod
    def cast_to_ticket_command(
        cmd_type,
        brand_id: int | None,
        description: str,
        fields: Iterable[CustomField],
        group_id: int | None,
        organization_id: int | None,
        priority: str,
        problem_id: int | None,
        requester_id: int | None,
        subject: str,
        tags: Iterable[str],
        ticket_form_id: int | None,
        ticket_type: str,
    ) -> TicketCmd:
        entity = cmd_type(
            subject=subject,
            custom_fields=fields,
            description=description,
            priority=priority,
            type=ticket_type,
            group_id=group_id,
            requester_id=requester_id,
            organization_id=organization_id,
            problem_id=problem_id,
            tags=tags,
            ticket_form_id=ticket_form_id,
            brand_id=brand_id,
        )
        return entity

    def show_multiple_tickets(self, ticket_ids: Iterable[int]) -> Iterable[Ticket]:
        return self._client.show_multiple_tickets(ticket_ids=ticket_ids)

    def update(
        self,
        ticket_id: int,
        subject: str = None,
        description: str = None,
        tags: Iterable[str] = (),
        custom_fields: Iterable[dict] = (),
        priority: str = "",
        ticket_type: str = "",
        group_id: int = None,
        requester_id: int = None,
        organization_id: int = None,
        problem_id: int = None,
        ticket_form_id: int = None,
        brand_id: int = None,
    ) -> Ticket:
        fields = []
        for custom_field in custom_fields:
            field = CustomField(id=custom_field["id"], value=custom_field["value"])
            fields.append(field)

        entity = self.cast_to_ticket_command(
            UpdateTicketCmd,
            brand_id,
            description,
            fields,
            group_id,
            organization_id,
            priority,
            problem_id,
            requester_id,
            subject,
            tags,
            ticket_form_id,
            ticket_type,
        )
        return self._client.update_ticket(ticket_id=ticket_id, entity=entity)

    def update_many(self, ticket_ids: Iterable[int], **fields) -> JobStatus:
        entity = UpdateTicketCmd(**fields)
        return self._client.update_many(ticket_ids=ticket_ids, entity=entity)

    def update_many_individually(self, updates: Iterable[tuple[int, dict]]) -> JobStatus:
        pairs = [(ticket_id, UpdateTicketCmd(**fields)) for ticket_id, fields in updates]
        return self._client.update_many_individually(updates=pairs)

    def delete(self, ticket_id: int) -> None:
        self._client.delete(ticket_id=ticket_id)

    def destroy_many(self, ticket_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(ticket_ids=ticket_ids)

    def mark_as_spam(self, ticket_id: int) -> None:
        self._client.mark_as_spam(ticket_id=ticket_id)

    def mark_many_as_spam(self, ticket_ids: Iterable[int]) -> JobStatus:
        return self._client.mark_many_as_spam(ticket_ids=ticket_ids)

    def merge(
        self,
        target_ticket_id: int,
        source_ids: Iterable[int],
        target_comment: str | None = None,
        source_comment: str | None = None,
        target_comment_is_public: bool = False,
        source_comment_is_public: bool = False,
    ) -> JobStatus:
        entity = MergeTicketsCmd(
            source_ids=source_ids,
            target_comment=target_comment,
            source_comment=source_comment,
            target_comment_is_public=target_comment_is_public,
            source_comment_is_public=source_comment_is_public,
        )
        return self._client.merge(target_ticket_id=target_ticket_id, entity=entity)

    def list_related(self, ticket_id: int) -> TicketRelated:
        return self._client.list_related(ticket_id=ticket_id)

    def list_deleted(self) -> Iterable[Ticket]:
        return self._client.list_deleted()

    def restore(self, ticket_id: int) -> None:
        self._client.restore(ticket_id=ticket_id)

    def restore_many(self, ticket_ids: Iterable[int]) -> None:
        self._client.restore_many(ticket_ids=ticket_ids)

    def permanently_delete(self, ticket_id: int) -> JobStatus:
        return self._client.permanently_delete(ticket_id=ticket_id)

    def permanently_delete_many(self, ticket_ids: Iterable[int]) -> JobStatus:
        return self._client.permanently_delete_many(ticket_ids=ticket_ids)

    def problems_autocomplete(self, text: str) -> Iterable[ProblemMatch]:
        return self._client.problems_autocomplete(text=text)

    def list_tags(self, ticket_id: int) -> list[str]:
        return self._client.list_tags(ticket_id=ticket_id)

    def set_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.set_tags(ticket_id=ticket_id, tags=tags)

    def add_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.add_tags(ticket_id=ticket_id, tags=tags)

    def remove_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        return self._client.remove_tags(ticket_id=ticket_id, tags=tags)

    def create_many(self, dict_input: Iterable[dict]) -> Iterable[Ticket]:
        entity = []
        for item in dict_input:
            record = self.cast_to_ticket_command(
                CreateTicketCmd,
                brand_id=item.get("brand_id"),
                description=item["description"],
                fields=[CustomField(id=cf["id"], value=cf["value"]) for cf in item.get("custom_fields", [])],
                group_id=item.get("group_id"),
                organization_id=item.get("organization_id"),
                priority=item.get("priority", ""),
                problem_id=item.get("problem_id"),
                requester_id=item.get("requester_id"),
                subject=item["subject"],
                tags=item.get("tags", ()),
                ticket_form_id=item.get("ticket_form_id"),
                ticket_type=item.get("type", ""),
            )
            entity.append(record)
        return self._client.create_many(entity=entity)
