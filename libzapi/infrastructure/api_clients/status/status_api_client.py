from __future__ import annotations
from typing import Iterable

from libzapi.domain.models.status.incident import Incident
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.serialization.parse import to_domain


def _flatten_incident(item: dict, included: list[dict]) -> dict:
    """Flatten a JSON:API incident resource and resolve included sideloads."""
    flat = {"id": item["id"], **item.get("attributes", {})}

    # Build lookup maps from included resources
    updates_by_id: dict[str, dict] = {}
    incident_services: list[dict] = []
    services_by_id: dict[str, dict] = {}

    for inc in included:
        inc_type = inc.get("type", "")
        inc_attrs = inc.get("attributes", {})
        if inc_type == "incident_update":
            updates_by_id[inc["id"]] = {"id": inc["id"], **inc_attrs}
        elif inc_type == "incident_service":
            incident_services.append({"id": inc["id"], **inc_attrs})
        elif inc_type == "service":
            services_by_id[inc["id"]] = {"id": inc["id"], **inc_attrs}

    # Resolve updates related to this incident
    rel_updates = item.get("relationships", {}).get("incident_updates", {}).get("data", [])
    flat["updates"] = [updates_by_id[u["id"]] for u in rel_updates if u["id"] in updates_by_id]

    # Resolve services related to this incident
    related_service_ids = set()
    for isvc in incident_services:
        if isvc.get("incident_id") == item["id"]:
            sid = isvc.get("service_id")
            if sid:
                related_service_ids.add(sid)
    flat["services"] = [services_by_id[sid] for sid in related_service_ids if sid in services_by_id]

    return flat


class StatusApiClient:
    """HTTP adapter for Zendesk Status API (public, no auth required).

    Base URL: https://status.zendesk.com
    Rate limit: 10 requests per minute.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_active(self, subdomain: str | None = None) -> Iterable[Incident]:
        path = "/api/incidents/active"
        if subdomain:
            path = f"{path}?subdomain={subdomain}"
        data = self._http.get(path)
        included = data.get("included", [])
        for item in data.get("data", []):
            yield to_domain(data=_flatten_incident(item, included), cls=Incident)

    def list_maintenance(self, subdomain: str | None = None) -> Iterable[Incident]:
        path = "/api/incidents/maintenance"
        if subdomain:
            path = f"{path}?subdomain={subdomain}"
        data = self._http.get(path)
        included = data.get("included", [])
        for item in data.get("data", []):
            yield to_domain(data=_flatten_incident(item, included), cls=Incident)

    def get(self, incident_id: str) -> Incident:
        path = f"/api/incidents/{incident_id}?include[]=incident_updates&include[]=incident_services&include[]=incident_services.service"
        data = self._http.get(path)
        included = data.get("included", [])
        item = data["data"]
        if isinstance(item, list):
            item = item[0]
        return to_domain(data=_flatten_incident(item, included), cls=Incident)
