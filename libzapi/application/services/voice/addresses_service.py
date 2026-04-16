from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.address_cmds import CreateAddressCmd, UpdateAddressCmd
from libzapi.domain.models.voice.address import Address
from libzapi.infrastructure.api_clients.voice.address_api_client import AddressApiClient


class AddressesService:
    def __init__(self, client: AddressApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[Address]:
        return self._client.list_all()

    def get(self, address_id: int) -> Address:
        return self._client.get(address_id=address_id)

    def create(
        self, city: str, country_code: str, name: str, province: str, street: str, zip: str, **kwargs
    ) -> Address:
        cmd = CreateAddressCmd(
            city=city, country_code=country_code, name=name, province=province, street=street, zip=zip, **kwargs
        )
        return self._client.create(cmd=cmd)

    def update(self, address_id: int, **kwargs) -> Address:
        cmd = UpdateAddressCmd(**kwargs)
        return self._client.update(address_id=address_id, cmd=cmd)

    def delete(self, address_id: int) -> None:
        self._client.delete(address_id=address_id)
