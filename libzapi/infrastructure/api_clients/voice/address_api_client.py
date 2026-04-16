from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.address_cmds import (
    CreateAddressCmd,
    UpdateAddressCmd,
)
from libzapi.domain.models.voice.address import Address
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.mappers.voice.address_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/addresses"


class AddressApiClient:
    """HTTP adapter for Zendesk Voice Addresses"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[Address]:
        data = self._http.get(_BASE)
        for obj in data["addresses"]:
            yield to_domain(data=obj, cls=Address)

    def get(self, address_id: int) -> Address:
        data = self._http.get(f"{_BASE}/{int(address_id)}")
        return to_domain(data=data["address"], cls=Address)

    def create(self, cmd: CreateAddressCmd) -> Address:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["address"], cls=Address)

    def update(self, address_id: int, cmd: UpdateAddressCmd) -> Address:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{int(address_id)}", json=payload)
        return to_domain(data=data["address"], cls=Address)

    def delete(self, address_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(address_id)}")
