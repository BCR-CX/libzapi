from __future__ import annotations

from typing import Iterable, Iterator, Optional

from libzapi.application.commands.ticketing.organization_cmds import (
    CreateOrganizationCmd,
    UpdateOrganizationCmd,
)
from libzapi.domain.models.ticketing.organization import Organization, OrganizationRelated
from libzapi.domain.shared_objects.count_snapshot import CountSnapshot
from libzapi.domain.shared_objects.job_status import JobStatus
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.count_mapper import to_count_snapshot
from libzapi.infrastructure.mappers.ticketing.organization_mapper import (
    to_payload_create,
    to_payload_update,
)
from libzapi.infrastructure.serialization.parse import to_domain


class OrganizationApiClient:
    """HTTP adapter for Zendesk Organizations"""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Iterator[Organization]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/organizations",
            base_url=self._http.base_url,
            items_key="organizations",
        ):
            yield to_domain(data=obj, cls=Organization)

    def list_organizations(self, user_id: int) -> Iterator[Organization]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path=f"/api/v2/users/{user_id}/organizations",
            base_url=self._http.base_url,
            items_key="organizations",
        ):
            yield to_domain(data=obj, cls=Organization)

    def get(self, organization_id: int) -> Organization:
        data = self._http.get(f"/api/v2/organizations/{int(organization_id)}")
        return to_domain(data=data["organization"], cls=Organization)

    def show_many(
        self,
        organization_ids: Optional[Iterable[int]] = None,
        external_ids: Optional[Iterable[str]] = None,
    ) -> Iterator[Organization]:
        if organization_ids is not None:
            ids_str = ",".join(str(int(i)) for i in organization_ids)
            path = f"/api/v2/organizations/show_many?ids={ids_str}"
        elif external_ids is not None:
            ext_str = ",".join(str(e) for e in external_ids)
            path = f"/api/v2/organizations/show_many?external_ids={ext_str}"
        else:
            raise ValueError("Either organization_ids or external_ids must be provided.")
        data = self._http.get(path)
        for obj in data.get("organizations", []):
            yield to_domain(data=obj, cls=Organization)

    def search(
        self, external_id: Optional[str] = None, name: Optional[str] = None
    ) -> Iterator[Organization]:
        if not external_id and not name:
            raise ValueError("Either external_id or name must be provided for search.")
        if external_id:
            search_term = "external_id"
            search_value = external_id
        else:
            search_term = "name"
            search_value = name
        data = self._http.get(f"/api/v2/organizations/search?{search_term}={search_value}")
        for obj in data.get("organizations", []) or []:
            yield to_domain(data=obj, cls=Organization)

    def autocomplete(self, name: str) -> Iterator[Organization]:
        data = self._http.get(f"/api/v2/organizations/autocomplete?name={name}")
        for obj in data.get("organizations", []):
            yield to_domain(data=obj, cls=Organization)

    def list_related(self, organization_id: int) -> OrganizationRelated:
        data = self._http.get(f"/api/v2/organizations/{int(organization_id)}/related")
        return to_domain(data=data["organization_related"], cls=OrganizationRelated)

    def count(self) -> CountSnapshot:
        data = self._http.get("/api/v2/organizations/count")
        return to_count_snapshot(data["count"])

    def create(self, entity: CreateOrganizationCmd) -> Organization:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/organizations", payload)
        return to_domain(data=data["organization"], cls=Organization)

    def update(self, organization_id: int, entity: UpdateOrganizationCmd) -> Organization:
        payload = to_payload_update(entity)
        data = self._http.put(f"/api/v2/organizations/{int(organization_id)}", payload)
        return to_domain(data=data["organization"], cls=Organization)

    def delete(self, organization_id: int) -> None:
        self._http.delete(f"/api/v2/organizations/{int(organization_id)}")

    def create_many(self, entities: Iterable[CreateOrganizationCmd]) -> JobStatus:
        payload = {
            "organizations": [to_payload_create(e)["organization"] for e in entities]
        }
        data = self._http.post("/api/v2/organizations/create_many", payload)
        return to_domain(data=data["job_status"], cls=JobStatus)

    def create_or_update(self, entity: CreateOrganizationCmd) -> Organization:
        payload = to_payload_create(entity)
        data = self._http.post("/api/v2/organizations/create_or_update", payload)
        return to_domain(data=data["organization"], cls=Organization)

    def update_many(
        self, organization_ids: Iterable[int], entity: UpdateOrganizationCmd
    ) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in organization_ids)
        payload = to_payload_update(entity)
        data = self._http.put(
            f"/api/v2/organizations/update_many?ids={ids_str}", payload
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def update_many_individually(
        self, updates: Iterable[tuple[int, UpdateOrganizationCmd]]
    ) -> JobStatus:
        orgs = []
        for organization_id, cmd in updates:
            org_payload = to_payload_update(cmd)["organization"]
            org_payload["id"] = int(organization_id)
            orgs.append(org_payload)
        data = self._http.put(
            "/api/v2/organizations/update_many", {"organizations": orgs}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def destroy_many(self, organization_ids: Iterable[int]) -> JobStatus:
        ids_str = ",".join(str(int(i)) for i in organization_ids)
        data = (
            self._http.delete(f"/api/v2/organizations/destroy_many?ids={ids_str}") or {}
        )
        return to_domain(data=data["job_status"], cls=JobStatus)

    def list_tags(self, organization_id: int) -> list[str]:
        data = self._http.get(f"/api/v2/organizations/{int(organization_id)}/tags")
        return list(data.get("tags", []))

    def set_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.post(
            f"/api/v2/organizations/{int(organization_id)}/tags", {"tags": list(tags)}
        )
        return list(data.get("tags", []))

    def add_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.put(
            f"/api/v2/organizations/{int(organization_id)}/tags", {"tags": list(tags)}
        )
        return list(data.get("tags", []))

    def remove_tags(self, organization_id: int, tags: Iterable[str]) -> list[str]:
        data = self._http.delete(
            f"/api/v2/organizations/{int(organization_id)}/tags",
            json={"tags": list(tags)},
        )
        return list((data or {}).get("tags", []))
