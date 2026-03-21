from __future__ import annotations
from typing import Iterator
from libzapi.application.commands.help_center.redirect_rule_cmds import CreateRedirectRuleCmd
from libzapi.domain.models.help_center.redirect_rule import RedirectRule
from libzapi.infrastructure.http.client import HttpClient
from libzapi.infrastructure.http.pagination import yield_items
from libzapi.infrastructure.mappers.help_center.redirect_rule_mapper import to_payload_create
from libzapi.infrastructure.serialization.parse import to_domain


class RedirectRuleApiClient:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_all(self) -> Iterator[RedirectRule]:
        for obj in yield_items(
            get_json=self._http.get,
            first_path="/api/v2/guide/redirect_rules",
            base_url=self._http.base_url,
            items_key="redirect_rules",
        ):
            yield to_domain(data=obj, cls=RedirectRule)

    def get(self, redirect_rule_id: str) -> RedirectRule:
        data = self._http.get(f"/api/v2/guide/redirect_rules/{redirect_rule_id}")
        return to_domain(data=data["redirect_rule"], cls=RedirectRule)

    def create(self, cmd: CreateRedirectRuleCmd) -> None:
        payload = to_payload_create(cmd)
        self._http.post("/api/v2/guide/redirect_rules", json=payload)

    def delete(self, redirect_rule_id: str) -> None:
        self._http.delete(f"/api/v2/guide/redirect_rules/{redirect_rule_id}")
