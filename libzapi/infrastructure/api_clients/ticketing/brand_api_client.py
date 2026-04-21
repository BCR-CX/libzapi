from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.brand_cmds import (
    CreateBrandCmd,
    UpdateBrandCmd,
)
from libzapi.domain.models.ticketing.brand import Brand
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.brand_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class BrandApiClient:
    """HTTP adapter for Zendesk Brands"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Brand]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/brands",
            base_url=self._http.base_url,
            items_key="brands",
        ):
            yield to_domain(data=obj, cls=Brand)

    def get(self, brand_id: int) -> Brand:
        data = self._http.get(f"/api/v2/brands/{int(brand_id)}")
        return to_domain(data=data["brand"], cls=Brand)

    def create(self, entity: CreateBrandCmd) -> Brand:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/brands", payload)
        return to_domain(data=data["brand"], cls=Brand)

    def update(self, brand_id: int, entity: UpdateBrandCmd) -> Brand:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/brands/{int(brand_id)}", payload)
        return to_domain(data=data["brand"], cls=Brand)

    def delete(self, brand_id: int) -> None:
        self._http.delete(f"/api/v2/brands/{int(brand_id)}")

    def check_host_mapping(self, host_mapping: str, subdomain: str) -> dict:
        return self._http.get(
            f"/api/v2/brands/check_host_mapping?host_mapping={host_mapping}&subdomain={subdomain}"
        )
