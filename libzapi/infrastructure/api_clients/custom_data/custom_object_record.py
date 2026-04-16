from typing import Iterator, TypeAlias, Literal, Iterable

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
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.custom_data.custom_object_record_mapper import (
    to_payload_bulk_job,
    to_payload_create,
    to_payload_filtered_search,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain

_ALLOWED_SORT_TYPES = {"id", "updated_at"}
_ALLOWED_SORT_ORDERS = {"asc", "desc"}

SortType: TypeAlias = Literal["id", "updated_at"]
SortOrder: TypeAlias = Literal["asc", "desc"]

_BASE = "/api/v2/custom_objects"


class CustomObjectRecordApiClient:
    """HTTP adapter for Zendesk Custom Objects Records API."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(
        self,
        custom_object_key: str,
        external_ids: Iterable,
        ids: Iterable,
        page_size: int,
        sort_type: SortType,
        sort_order: SortOrder,
    ) -> Iterator[CustomObjectRecord]:
        query = build_query(
            external_ids=external_ids, ids=ids, page_size=page_size, sort_type=sort_type, sort_order=sort_order
        )
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/{custom_object_key}/records?{query}",
            base_url=self._http.base_url,
            items_key="custom_object_records",
        ):
            yield to_domain(data=obj, cls=CustomObjectRecord)

    def get(self, custom_object_key: str, custom_object_record_id: str) -> CustomObjectRecord:
        data = self._http.get(f"{_BASE}/{custom_object_key}/records/{custom_object_record_id}")
        return to_domain(data=data["custom_object_record"], cls=CustomObjectRecord)

    def create(self, custom_object_key: str, cmd: CreateCustomObjectRecordCmd) -> CustomObjectRecord:
        payload = to_payload_create(cmd)
        data = self._http.post(f"{_BASE}/{custom_object_key}/records", json=payload)
        return to_domain(data=data["custom_object_record"], cls=CustomObjectRecord)

    def update(self, custom_object_key: str, record_id: str, cmd: UpdateCustomObjectRecordCmd) -> CustomObjectRecord:
        payload = to_payload_update(cmd)
        data = self._http.patch(f"{_BASE}/{custom_object_key}/records/{record_id}", json=payload)
        return to_domain(data=data["custom_object_record"], cls=CustomObjectRecord)

    def upsert(
        self,
        custom_object_key: str,
        cmd: CreateCustomObjectRecordCmd,
        *,
        external_id: str | None = None,
        name: str | None = None,
    ) -> CustomObjectRecord:
        payload = to_payload_create(cmd)
        path = f"{_BASE}/{custom_object_key}/records"
        if external_id:
            path = f"{path}?external_id={external_id}"
        elif name:
            path = f"{path}?name={name}"
        data = self._http.patch(path, json=payload)
        return to_domain(data=data["custom_object_record"], cls=CustomObjectRecord)

    def delete(self, custom_object_key: str, record_id: str) -> None:
        self._http.delete(f"{_BASE}/{custom_object_key}/records/{record_id}")

    def delete_by_external_id(self, custom_object_key: str, external_id: str) -> None:
        self._http.delete(f"{_BASE}/{custom_object_key}/records?external_id={external_id}")

    def delete_by_name(self, custom_object_key: str, name: str) -> None:
        self._http.delete(f"{_BASE}/{custom_object_key}/records?name={name}")

    def count(self, custom_object_key: str) -> CountSnapshot:
        data = self._http.get(f"{_BASE}/{custom_object_key}/records/count")
        return to_domain(data=data["count"], cls=CountSnapshot)

    def search(self, custom_object_key: str, query: str, sort: str | None = None) -> Iterator[CustomObjectRecord]:
        path = f"{_BASE}/{custom_object_key}/records/search?query={query}"
        if sort:
            path = f"{path}&sort={sort}"
        for obj in yield_items(
            get_json=self._http.get,
            first_path=path,
            base_url=self._http.base_url,
            items_key="custom_object_records",
        ):
            yield to_domain(data=obj, cls=CustomObjectRecord)

    def filtered_search(self, custom_object_key: str, cmd: FilteredSearchCmd) -> Iterator[CustomObjectRecord]:
        payload = to_payload_filtered_search(cmd)
        data = self._http.post(f"{_BASE}/{custom_object_key}/records/search", json=payload)
        for obj in data.get("custom_object_records", []):
            yield to_domain(data=obj, cls=CustomObjectRecord)

    def autocomplete(self, custom_object_key: str, name: str) -> Iterator[CustomObjectRecord]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"{_BASE}/{custom_object_key}/records/autocomplete?name={name}",
            base_url=self._http.base_url,
            items_key="custom_object_records",
        ):
            yield to_domain(data=obj, cls=CustomObjectRecord)

    def bulk_job(self, custom_object_key: str, cmd: BulkJobCmd) -> JobStatus:
        payload = to_payload_bulk_job(cmd)
        data = self._http.post(f"{_BASE}/{custom_object_key}/jobs", json=payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def incremental_export(self, custom_object_key: str, start_time: int) -> Iterator[CustomObjectRecord]:
        path = f"/api/v2/incremental/custom_objects/{custom_object_key}/cursor?start_time={int(start_time)}"
        while path:
            data = self._http.get(path)
            for obj in data.get("custom_object_records", []):
                yield to_domain(data=obj, cls=CustomObjectRecord)
            if data.get("end_of_stream"):
                break
            after_url = data.get("links", {}).get("next")
            if after_url and isinstance(after_url, str):
                path = after_url.replace(self._http.base_url, "") if after_url.startswith("https://") else after_url
            else:
                path = None

    def limit(self) -> CustomObjectLimit:
        data = self._http.get(f"{_BASE}/limits/record_limit")
        return to_domain(data=data, cls=CustomObjectLimit)


def build_query(
    external_ids: Iterable, ids: Iterable, page_size: int, sort_type: SortType, sort_order: SortOrder
) -> str:
    query_parts = []
    if sort_type not in _ALLOWED_SORT_TYPES:
        raise ValueError(f"Invalid sort_type: {sort_type}")

    if sort_order not in _ALLOWED_SORT_ORDERS:
        raise ValueError(f"Invalid sort_order: {sort_order}")

    if external_ids:
        external_ids_str = ",".join(external_ids)
        query_parts.append(f"filter[external_ids]={external_ids_str}")
    if ids:
        ids_str = ",".join(ids)
        query_parts.append(f"filter[ids]={ids_str}")
    if page_size:
        query_parts.append(f"page[size]={page_size}")
    if sort_type:
        sort_prefix = "" if sort_order == "asc" else "-"
        query_parts.append(f"sort={sort_prefix}{sort_type}")
    return "&".join(query_parts)
