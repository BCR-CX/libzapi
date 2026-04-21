from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.support_address_cmds import (
    CreateSupportAddressCmd,
    UpdateSupportAddressCmd,
)
from libzapi.domain.models.ticketing.support_address import RecipientAddress
from libzapi.infrastructure.api_clients.ticketing.support_address_api_client import (
    SupportAddressApiClient,
)


class SupportAddressesService:
    """High-level service using the API client."""

    def __init__(self, client: SupportAddressApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[RecipientAddress]:
        return self._client.list()

    def get(self, support_address_id: int) -> RecipientAddress:
        return self._client.get(support_address_id)

    def create(self, **fields) -> RecipientAddress:
        return self._client.create(entity=CreateSupportAddressCmd(**fields))

    def update(self, support_address_id: int, **fields) -> RecipientAddress:
        return self._client.update(
            support_address_id=support_address_id,
            entity=UpdateSupportAddressCmd(**fields),
        )

    def delete(self, support_address_id: int) -> None:
        self._client.delete(support_address_id=support_address_id)

    def verify(self, support_address_id: int) -> dict:
        return self._client.verify(support_address_id=support_address_id)
