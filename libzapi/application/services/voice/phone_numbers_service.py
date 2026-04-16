from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.phone_number_cmds import CreatePhoneNumberCmd, UpdatePhoneNumberCmd
from libzapi.domain.models.voice.phone_number import AvailablePhoneNumber, PhoneNumber
from libzapi.infrastructure.api_clients.voice.phone_number_api_client import PhoneNumberApiClient


class PhoneNumbersService:
    def __init__(self, client: PhoneNumberApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterator[PhoneNumber]:
        return self._client.list_all()

    def search(
        self,
        country: str,
        area_code: str | None = None,
        contains: str | None = None,
        toll_free: bool | None = None,
    ) -> list[AvailablePhoneNumber]:
        return self._client.search(country=country, area_code=area_code, contains=contains, toll_free=toll_free)

    def get(self, phone_number_id: int) -> PhoneNumber:
        return self._client.get(phone_number_id=phone_number_id)

    def create(self, token: str, nickname: str = "", address_sid: str | None = None) -> PhoneNumber:
        cmd = CreatePhoneNumberCmd(token=token, nickname=nickname, address_sid=address_sid)
        return self._client.create(cmd=cmd)

    def update(self, phone_number_id: int, **kwargs) -> PhoneNumber:
        cmd = UpdatePhoneNumberCmd(**kwargs)
        return self._client.update(phone_number_id=phone_number_id, cmd=cmd)

    def delete(self, phone_number_id: int) -> None:
        self._client.delete(phone_number_id=phone_number_id)
