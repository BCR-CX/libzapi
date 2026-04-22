from __future__ import annotations

from typing import Iterator, List, Optional

from libzapi.application.commands.ticketing.dynamic_content_cmds import (
    CreateDynamicContentItemCmd,
    CreateDynamicContentVariantCmd,
    DynamicContentVariantInputCmd,
    UpdateDynamicContentItemCmd,
    UpdateDynamicContentVariantCmd,
)
from libzapi.domain.models.ticketing.dynamic_content import (
    DynamicContentItem,
    DynamicContentVariant,
)
from libzapi.infrastructure.api_clients.ticketing.dynamic_content_api_client import (
    DynamicContentApiClient,
)


class DynamicContentService:
    def __init__(self, client: DynamicContentApiClient) -> None:
        self._client = client

    def list_items(self) -> Iterator[DynamicContentItem]:
        return self._client.list_items()

    def get_item(self, item_id: int) -> DynamicContentItem:
        return self._client.get_item(item_id=item_id)

    def create_item(
        self,
        *,
        name: str,
        default_locale_id: int,
        variants: Optional[List[DynamicContentVariantInputCmd]] = None,
    ) -> DynamicContentItem:
        cmd = CreateDynamicContentItemCmd(
            name=name,
            default_locale_id=default_locale_id,
            variants=list(variants) if variants else [],
        )
        return self._client.create_item(entity=cmd)

    def update_item(
        self, item_id: int, *, name: Optional[str] = None
    ) -> DynamicContentItem:
        cmd = UpdateDynamicContentItemCmd(name=name)
        return self._client.update_item(item_id=item_id, entity=cmd)

    def delete_item(self, item_id: int) -> None:
        self._client.delete_item(item_id=item_id)

    def list_variants(self, item_id: int) -> Iterator[DynamicContentVariant]:
        return self._client.list_variants(item_id=item_id)

    def get_variant(
        self, item_id: int, variant_id: int
    ) -> DynamicContentVariant:
        return self._client.get_variant(item_id=item_id, variant_id=variant_id)

    def create_variant(
        self,
        item_id: int,
        *,
        content: str,
        locale_id: int,
        default: Optional[bool] = None,
        active: Optional[bool] = None,
    ) -> DynamicContentVariant:
        cmd = CreateDynamicContentVariantCmd(
            content=content,
            locale_id=locale_id,
            default=default,
            active=active,
        )
        return self._client.create_variant(item_id=item_id, entity=cmd)

    def update_variant(
        self,
        item_id: int,
        variant_id: int,
        *,
        content: Optional[str] = None,
        locale_id: Optional[int] = None,
        default: Optional[bool] = None,
        active: Optional[bool] = None,
    ) -> DynamicContentVariant:
        cmd = UpdateDynamicContentVariantCmd(
            content=content,
            locale_id=locale_id,
            default=default,
            active=active,
        )
        return self._client.update_variant(
            item_id=item_id, variant_id=variant_id, entity=cmd
        )

    def delete_variant(self, item_id: int, variant_id: int) -> None:
        self._client.delete_variant(item_id=item_id, variant_id=variant_id)
