from __future__ import annotations

from typing import Iterator, Optional, Iterable

from libzapi.application.commands.custom_data.custom_object_record_cmds import (
    BulkJobCmd,
    CreateCustomObjectRecordCmd,
    FilteredSearchCmd,
    UpdateCustomObjectRecordCmd,
)
from libzapi.domain.models.custom_data.custom_object_record import CustomObjectRecord
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.custom_object_limit import CustomObjectLimit
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.api_clients.custom_data import CustomObjectRecordApiClient
from libzapi.infrastructure.api_clients.custom_data.custom_object_record import SortOrder, SortType


class CustomObjectRecordsService:
    """High-level service using the API client."""

    def __init__(self, client: CustomObjectRecordApiClient) -> None:
        self._client = client

    def list_all(
        self,
        custom_object_key: str,
        external_ids: Optional[Iterable[str]] = None,
        ids: Optional[Iterable[str]] = None,
        page_size: int = 100,
        sort_type: SortType = "id",
        sort_order: SortOrder = "desc",
    ) -> Iterator[CustomObjectRecord]:
        return self._client.list_all(custom_object_key, external_ids, ids, page_size, sort_type, sort_order)

    def get(self, custom_object_key: str, custom_object_record_id: str) -> CustomObjectRecord:
        return self._client.get(custom_object_key=custom_object_key, custom_object_record_id=custom_object_record_id)

    def create(
        self, custom_object_key: str, name: str, custom_object_fields: dict[str, str] | None = None, **kwargs
    ) -> CustomObjectRecord:
        cmd = CreateCustomObjectRecordCmd(name=name, custom_object_fields=custom_object_fields or {}, **kwargs)
        return self._client.create(custom_object_key=custom_object_key, cmd=cmd)

    def update(
        self, custom_object_key: str, record_id: str, custom_object_fields: dict[str, str]
    ) -> CustomObjectRecord:
        cmd = UpdateCustomObjectRecordCmd(custom_object_fields=custom_object_fields)
        return self._client.update(custom_object_key=custom_object_key, record_id=record_id, cmd=cmd)

    def upsert(
        self,
        custom_object_key: str,
        name: str,
        custom_object_fields: dict[str, str] | None = None,
        *,
        external_id: str | None = None,
        upsert_by_name: str | None = None,
        **kwargs,
    ) -> CustomObjectRecord:
        cmd = CreateCustomObjectRecordCmd(name=name, custom_object_fields=custom_object_fields or {}, **kwargs)
        return self._client.upsert(
            custom_object_key=custom_object_key, cmd=cmd, external_id=external_id, name=upsert_by_name
        )

    def delete(self, custom_object_key: str, record_id: str) -> None:
        self._client.delete(custom_object_key=custom_object_key, record_id=record_id)

    def delete_by_external_id(self, custom_object_key: str, external_id: str) -> None:
        self._client.delete_by_external_id(custom_object_key=custom_object_key, external_id=external_id)

    def delete_by_name(self, custom_object_key: str, name: str) -> None:
        self._client.delete_by_name(custom_object_key=custom_object_key, name=name)

    def count(self, custom_object_key: str) -> CountSnapshot:
        return self._client.count(custom_object_key=custom_object_key)

    def search(self, custom_object_key: str, query: str, sort: str | None = None) -> Iterator[CustomObjectRecord]:
        return self._client.search(custom_object_key=custom_object_key, query=query, sort=sort)

    def filtered_search(self, custom_object_key: str, filter: dict) -> Iterator[CustomObjectRecord]:
        cmd = FilteredSearchCmd(filter=filter)
        return self._client.filtered_search(custom_object_key=custom_object_key, cmd=cmd)

    def autocomplete(self, custom_object_key: str, name: str) -> Iterator[CustomObjectRecord]:
        return self._client.autocomplete(custom_object_key=custom_object_key, name=name)

    def bulk_job(self, custom_object_key: str, action: str, items: list[dict]) -> JobStatus:
        cmd = BulkJobCmd(action=action, items=items)
        return self._client.bulk_job(custom_object_key=custom_object_key, cmd=cmd)

    def incremental_export(self, custom_object_key: str, start_time: int) -> Iterator[CustomObjectRecord]:
        return self._client.incremental_export(custom_object_key=custom_object_key, start_time=start_time)

    def limit(self) -> CustomObjectLimit:
        return self._client.limit()
