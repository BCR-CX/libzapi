from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)
from libzapi.domain.models.ticketing.support_address import RecipientAddress
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.support_address_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class SupportAddressApiClient:
    """HTTP adapter for Zendesk Recipient Addresses."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[RecipientAddress]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/recipient_addresses",
            base_url=self._http.base_url,
            items_key="recipient_addresses",
        ):
            yield to_domain(data=obj, cls=RecipientAddress)

    def get(self, support_address_id: int) -> RecipientAddress:
        data = self._http.get(
            f"/api/v2/recipient_addresses/{int(support_address_id)}"
        )
        return to_domain(data=data["recipient_address"], cls=RecipientAddress)

    def create(self, entity: CreateSupportAddressCmd) -> RecipientAddress:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/recipient_addresses", payload)
        return to_domain(data=data["recipient_address"], cls=RecipientAddress)

    def update(
        self, support_address_id: int, entity: UpdateSupportAddressCmd
    ) -> RecipientAddress:
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/recipient_addresses/{int(support_address_id)}", payload
        )
        return to_domain(data=data["recipient_address"], cls=RecipientAddress)

    def delete(self, support_address_id: int) -> None:
        self._http.delete(
            f"/api/v2/recipient_addresses/{int(support_address_id)}"
        )

    def verify(self, support_address_id: int) -> dict:
        return self._http.put(
            f"/api/v2/recipient_addresses/{int(support_address_id)}/verify",
            {},
        )
