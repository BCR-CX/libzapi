from __future__ import annotations

from typing import Any, Iterable

from libzapi.application.commands.ticketing.macro_cmds import (
    CreateMacroCmd,
    UpdateMacroCmd,
)
from libzapi.domain.models.ticketing.macro import Macro
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.ticketing import MacroApiClient


class MacroService:
    """High-level service using the API client."""

    def __init__(self, client: MacroApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[Macro]:
        return self._client.list()

    def list_active(self) -> Iterable[Macro]:
        return self._client.list_active()

    def search(self, query: str) -> Iterable[Macro]:
        return self._client.search(query=query)

    def list_categories(self) -> list[str]:
        return self._client.list_categories()

    def list_definitions(self) -> dict:
        return self._client.list_definitions()

    def get(self, macro_id: int) -> Macro:
        return self._client.get(macro_id=macro_id)

    def apply(self, macro_id: int) -> dict:
        return self._client.apply(macro_id=macro_id)

    def apply_to_ticket(self, ticket_id: int, macro_id: int) -> dict:
        return self._client.apply_to_ticket(ticket_id=ticket_id, macro_id=macro_id)

    def create(self, **fields) -> Macro:
        return self._client.create(entity=CreateMacroCmd(**fields))

    def update(self, macro_id: int, **fields) -> Macro:
        return self._client.update(
            macro_id=macro_id, entity=UpdateMacroCmd(**fields)
        )

    def delete(self, macro_id: int) -> None:
        self._client.delete(macro_id=macro_id)

    def create_many(self, macros: Iterable[dict[str, Any]]) -> JobStatus:
        return self._client.create_many(
            entities=[CreateMacroCmd(**m) for m in macros]
        )

    def update_many(
        self, updates: Iterable[tuple[int, dict[str, Any]]]
    ) -> JobStatus:
        pairs = [
            (macro_id, UpdateMacroCmd(**fields))
            for macro_id, fields in updates
        ]
        return self._client.update_many(updates=pairs)

    def destroy_many(self, macro_ids: Iterable[int]) -> JobStatus:
        return self._client.destroy_many(macro_ids=macro_ids)
