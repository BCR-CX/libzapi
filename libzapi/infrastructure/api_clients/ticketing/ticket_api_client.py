from __future__ import annotations

from typing import Iterator, Iterable

from libzapi.domain.models.ticketing.ticket import ProblemMatch, Ticket, TicketRelated, User
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.serialization.parse import to_domain
from libzapi.infrastructure.mappers.ticketing.ticket_mapper import (
    to_payload_create,
    to_payload_merge,
    to_payload_update,
)
from libzapi.application.commands.ticketing.ticket_cmds import (
    CreateTicketCmd,
    MergeTicketsCmd,
    UpdateTicketCmd,
)


class TicketApiClient:
    """HTTP adapter for Zendesk Tickets"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Ticket]:
        data = self._http.get("/api/v2/tickets")
        for obj in data["tickets"]:
            yield to_domain(data=obj, cls=Ticket)

    def list_organization(self, organization_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/organizations/{int(organization_id)}/tickets")

    def list_user_requested(self, user_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/users/{int(user_id)}/tickets/requested")

    def list_user_ccd(self, user_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/users/{int(user_id)}/tickets/ccd")

    def list_user_followed(self, user_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/users/{int(user_id)}/tickets/followed")

    def list_user_assigned(self, user_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/users/{int(user_id)}/tickets/assigned")

    def list_recent(self) -> Iterator[Ticket]:
        return self._list_tickets(path="/api/v2/tickets/recent")

    def list_collaborators(self, ticket_id: int) -> Iterator[User]:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/collaborators")
        for obj in data["users"]:
            yield to_domain(data=obj, cls=User)

    def list_followers(self, ticket_id: int) -> Iterator[User]:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/followers")
        for obj in data["users"]:
            yield to_domain(data=obj, cls=User)

    def list_email_ccs(self, ticket_id: int) -> Iterator[User]:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/email_ccs")
        for obj in data["users"]:
            yield to_domain(data=obj, cls=User)

    def list_incidents(self, ticket_id: int) -> Iterator[Ticket]:
        return self._list_tickets(path=f"/api/v2/tickets/{int(ticket_id)}/incidents")

    def list_problems(self) -> Iterator[Ticket]:
        return self._list_tickets(path="/api/v2/tickets/problems")

    def get(self, ticket_id: int) -> Ticket:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}")
        return to_domain(data=data["ticket"], cls=Ticket)

    def count(self) -> CountSnapshot:
        data = self._http.get("/api/v2/tickets/count")
        return data["count"]

    def organization_count(self, organization_id: int) -> CountSnapshot:
        data = self._http.get(f"/api/v2/organizations/{int(organization_id)}/tickets/count")
        return data["count"]

    def user_ccd_count(self, user_id: int) -> CountSnapshot:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/tickets/ccd/count")
        return data["count"]

    def user_assigned_count(self, user_id: int) -> CountSnapshot:
        data = self._http.get(f"/api/v2/users/{int(user_id)}/tickets/assigned/count")
        return data["count"]

    def show_multiple_tickets(self, ticket_ids: Iterable[int]) -> Iterator[Ticket]:
        ids_str = ",".join(str(id_) for id_ in ticket_ids)
        data = self._http.get(f"/api/v2/tickets/show_many?ids={ids_str}")
        for obj in data["tickets"]:
            yield to_domain(data=obj, cls=Ticket)

    def create_ticket(self, entity: CreateTicketCmd) -> Ticket:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/tickets", payload)
        return to_domain(data=data["ticket"], cls=Ticket)

    def update_ticket(self, ticket_id: int, entity: UpdateTicketCmd) -> Ticket:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/tickets/{int(ticket_id)}", payload)
        return to_domain(data=data["ticket"], cls=Ticket)

    def create_many(self, entity: Iterable[CreateTicketCmd]) -> JobStatus:
        payload = {"tickets": [to_payload_create(e)["ticket"] for e in entity]}
        data = self._http.post("/api/v2/tickets/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many(self, ticket_ids: Iterable[int], entity: UpdateTicketCmd) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in ticket_ids)
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/tickets/update_many?ids={ids_str}", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many_individually(self, updates: Iterable[tuple[int, UpdateTicketCmd]]) -> JobStatus:
        tickets = []
        for ticket_id, cmd in updates:
            ticket_payload = to_payload_update(cmd)["ticket"]
            ticket_payload["id"] = int(ticket_id)
            tickets.append(ticket_payload)
        data = self._http.put("/api/v2/tickets/update_many", {"tickets": tickets})
        return to_domain(data=data["job_status"], cls=JobStatus)

    def delete(self, ticket_id: int) -> None:
        self._http.delete(f"/api/v2/tickets/{int(ticket_id)}")

    def destroy_many(self, ticket_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in ticket_ids)
        data = self._http.delete(f"/api/v2/tickets/destroy_many?ids={ids_str}") or {}
        return to_domain(data=data["job_status"], cls=JobStatus)

    def mark_as_spam(self, ticket_id: int) -> None:
        self._http.put(f"/api/v2/tickets/{int(ticket_id)}/mark_as_spam", {})

    def mark_many_as_spam(self, ticket_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in ticket_ids)
        data = self._http.put(f"/api/v2/tickets/mark_many_as_spam?ids={ids_str}", {})
        return to_domain(data=data["job_status"], cls=JobStatus)

    def merge(self, target_ticket_id: int, entity: MergeTicketsCmd) -> JobStatus:
        payload = to_payload_merge(entity)
        data = self._http.post(f"/api/v2/tickets/{int(target_ticket_id)}/merge", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def list_related(self, ticket_id: int) -> TicketRelated:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/related")
        return to_domain(data=data["ticket_related"], cls=TicketRelated)

    def list_deleted(self) -> Iterator[Ticket]:
        items = yield_items(
            get_json=self._http.get,
            first_path="/api/v2/deleted_tickets",
            base_url=self._http.base_url,
            items_key="deleted_tickets",
        )
        return (to_domain(data=obj, cls=Ticket) for obj in items)

    def restore(self, ticket_id: int) -> None:
        self._http.put(f"/api/v2/deleted_tickets/{int(ticket_id)}/restore", {})

    def restore_many(self, ticket_ids: Iterable[int]) -> None:
        ids_str = ",".join(str(int(i)) for i in ticket_ids)
        self._http.put(f"/api/v2/deleted_tickets/restore_many?ids={ids_str}", {})

    def permanently_delete(self, ticket_id: int) -> JobStatus:
        data = self._http.delete(f"/api/v2/deleted_tickets/{int(ticket_id)}") or {}
        return to_domain(data=data["job_status"], cls=JobStatus)

    def permanently_delete_many(self, ticket_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in ticket_ids)
        data = self._http.delete(f"/api/v2/deleted_tickets/destroy_many?ids={ids_str}") or {}
        return to_domain(data=data["job_status"], cls=JobStatus)

    def problems_autocomplete(self, text: str) -> Iterator[ProblemMatch]:
        data = self._http.post("/api/v2/problems/autocomplete", {"text": text})
        for obj in data["tickets"]:
            yield to_domain(data=obj, cls=ProblemMatch)

    def list_tags(self, ticket_id: int) -> list[str]:
        data = self._http.get(f"/api/v2/tickets/{int(ticket_id)}/tags")
        return list(data.get("tags", []))

    def set_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.post(f"/api/v2/tickets/{int(ticket_id)}/tags", {"tags": list(tags)})
        return list(data.get("tags", []))

    def add_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.put(f"/api/v2/tickets/{int(ticket_id)}/tags", {"tags": list(tags)})
        return list(data.get("tags", []))

    def remove_tags(self, ticket_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.delete(
            f"/api/v2/tickets/{int(ticket_id)}/tags", json={"tags": list(tags)}
        )
        return list((data or {}).get("tags", []))

    def _list_tickets(self, path: str) -> Iterator[Ticket]:
        """Helper to reduce code duplication for listing tickets."""
        items = yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="tickets",
        )
        return (to_domain(data=obj, cls=Ticket) for obj in items)
