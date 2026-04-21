from __future__ import annotations

from typing import Iterable

from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)
from libzapi.domain.models.ticketing.brand import Brand
from libzapi.infrastructure.api_clients.ticketing import BrandApiClient


class BrandsService:
    """High-level service using the API client."""

    def __init__(self, client: BrandApiClient) -> None:
        self._client = client

    def list(self) -> Iterable[Brand]:
        return self._client.list()

    def get(self, brand_id: int) -> Brand:
        return self._client.get(brand_id=brand_id)

    def create(self, **fields) -> Brand:
        return self._client.create(entity=CreateBrandCmd(**fields))

    def update(self, brand_id: int, **fields) -> Brand:
        return self._client.update(
            brand_id=brand_id, entity=UpdateBrandCmd(**fields)
        )

    def delete(self, brand_id: int) -> None:
        self._client.delete(brand_id=brand_id)

    def check_host_mapping(self, host_mapping: str, subdomain: str) -> dict:
        return self._client.check_host_mapping(
            host_mapping=host_mapping, subdomain=subdomain
        )
