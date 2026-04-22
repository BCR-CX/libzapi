from __future__ import annotations

from typing import Iterator

from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)
from libzapi.domain.models.ticketing.dynamic_content import (
    DynamicContentItem,
    DynamicContentVariant,
)
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.ticketing.dynamic_content_mapper import (
    to_payload_create_item,
    to_payload_create_variant,
    to_payload_update_item,
    to_payload_update_variant,
)
from libzapi.infrastructure.serialization.parse import to_domain

_ITEMS = "/api/v2/dynamic_content/items"


class DynamicContentApiClient:
    """HTTP adapter for Zendesk Dynamic Content."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_items(self) -> Iterator[DynamicContentItem]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=_ITEMS,
            base_url=self._http.base_url,
            items_key="items",
        ):
            yield to_domain(data=obj, cls=DynamicContentItem)

    def get_item(self, item_id: int) -> DynamicContentItem:
        data = self._http.get(f"{_ITEMS}/{int(item_id)}")
        return to_domain(data=data["item"], cls=DynamicContentItem)

    def create_item(
        self, entity: CreateDynamicContentItemCmd
    ) -> DynamicContentItem:
        data = self._http.post(_ITEMS, to_payload_create_item(entity))
        return to_domain(data=data["item"], cls=DynamicContentItem)

    def update_item(
        self, item_id: int, entity: UpdateDynamicContentItemCmd
    ) -> DynamicContentItem:
        data = self._http.put(
            f"{_ITEMS}/{int(item_id)}", to_payload_update_item(entity)
        )
        return to_domain(data=data["item"], cls=DynamicContentItem)

    def delete_item(self, item_id: int) -> None:
        self._http.delete(f"{_ITEMS}/{int(item_id)}")

    def list_variants(self, item_id: int) -> Iterator[DynamicContentVariant]:
        path = f"{_ITEMS}/{int(item_id)}/variants"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="variants",
        ):
            yield to_domain(data=obj, cls=DynamicContentVariant)

    def get_variant(self, item_id: int, variant_id: int) -> DynamicContentVariant:
        data = self._http.get(
            f"{_ITEMS}/{int(item_id)}/variants/{int(variant_id)}"
        )
        return to_domain(data=data["variant"], cls=DynamicContentVariant)

    def create_variant(
        self, item_id: int, entity: CreateDynamicContentVariantCmd
    ) -> DynamicContentVariant:
        data = self._http.post(
            f"{_ITEMS}/{int(item_id)}/variants",
            to_payload_create_variant(entity),
        )
        return to_domain(data=data["variant"], cls=DynamicContentVariant)

    def update_variant(
        self,
        item_id: int,
        variant_id: int,
        entity: UpdateDynamicContentVariantCmd,
    ) -> DynamicContentVariant:
        data = self._http.put(
            f"{_ITEMS}/{int(item_id)}/variants/{int(variant_id)}",
            to_payload_update_variant(entity),
        )
        return to_domain(data=data["variant"], cls=DynamicContentVariant)

    def delete_variant(self, item_id: int, variant_id: int) -> None:
        self._http.delete(f"{_ITEMS}/{int(item_id)}/variants/{int(variant_id)}")
