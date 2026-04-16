from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.voice.phone_number_cmds import (
    CreatePhoneNumberCmd,
    UpdatePhoneNumberCmd,
)
from libzapi.domain.models.voice.phone_number import AvailablePhoneNumber, PhoneNumber
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.voice.phone_number_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain

_BASE = "/api/v2/channels/voice/phone_numbers"


class PhoneNumberApiClient:
    """HTTP adapter for Zendesk Voice Phone Numbers"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[PhoneNumber]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_BASE,
            base_url=self._http.base_url,
            items_key="phone_numbers",
        ):
            yield to_domain(data=obj, cls=PhoneNumber)

    def search(
        self,
        country: str,
        area_code: str | None = None,
        contains: str | None = None,
        toll_free: bool | None = None,
    ) -> list[AvailablePhoneNumber]:
        params: dict[str, str] = {"country": country}
        if area_code is not None:
            params["area_code"] = area_code
        if contains is not None:
            params["contains"] = contains
        if toll_free is not None:
            params["toll_free"] = str(toll_free).lower()
        query = "&".join(f"{k}={v}" for k, v in params.items())
        data = self._http.get(f"{_BASE}/search?{query}")
        return [to_domain(data=obj, cls=AvailablePhoneNumber) for obj in data["phone_numbers"]]

    def get(self, phone_number_id: int) -> PhoneNumber:
        data = self._http.get(f"{_BASE}/{int(phone_number_id)}")
        return to_domain(data=data["phone_number"], cls=PhoneNumber)

    def create(self, cmd: CreatePhoneNumberCmd) -> PhoneNumber:
        payload = to_payload_create(cmd)
        data = self._http.post(_BASE, json=payload)
        return to_domain(data=data["phone_number"], cls=PhoneNumber)

    def update(self, phone_number_id: int, cmd: UpdatePhoneNumberCmd) -> PhoneNumber:
        payload = to_payload_update(cmd)
        data = self._http.put(f"{_BASE}/{int(phone_number_id)}", json=payload)
        return to_domain(data=data["phone_number"], cls=PhoneNumber)

    def delete(self, phone_number_id: int) -> None:
        self._http.delete(f"{_BASE}/{int(phone_number_id)}")
