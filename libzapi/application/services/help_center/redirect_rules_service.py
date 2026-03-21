from typing import Iterable
from libzapi.application.commands.help_center.redirect_rule_cmds import CreateRedirectRuleCmd
from libzapi.domain.models.help_center.redirect_rule import RedirectRule
from libzapi.infrastructure.api_clients.help_center.redirect_rule_api_client import RedirectRuleApiClient


class RedirectRulesService:
    def __init__(self, client: RedirectRuleApiClient) -> None:
        self._client = client

    def list_all(self) -> Iterable[RedirectRule]:
        return self._client.list_all()

    def get(self, redirect_rule_id: str) -> RedirectRule:
        return self._client.get(redirect_rule_id=redirect_rule_id)

    def create(self, brand_id: int, redirect_from: str, redirect_to: str, redirect_status: int = 301) -> None:
        cmd = CreateRedirectRuleCmd(
            brand_id=brand_id, redirect_from=redirect_from, redirect_to=redirect_to, redirect_status=redirect_status
        )
        self._client.create(cmd=cmd)

    def delete(self, redirect_rule_id: str) -> None:
        self._client.delete(redirect_rule_id=redirect_rule_id)
