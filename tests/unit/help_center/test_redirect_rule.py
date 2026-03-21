import pytest
from hypothesis.strategies import builds, just

from libzapi.domain.models.help_center.redirect_rule import RedirectRule
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.help_center import RedirectRuleApiClient
from hypothesis import given

strategy = builds(
    RedirectRule,
    id=just("cciiA"),
)


@given(strategy)
def test_session_logical_key_from_id(model: RedirectRule):
    assert model.logical_key.as_str() == "redirect_rule:id_cciia"


@pytest.mark.parametrize(
    "method_name, args, expected_path, items_key", [("list_all", [], "/api/v2/guide/redirect_rules", "redirect_rules")]
)
def test_redirect_rule_api_client_list(method_name, args, expected_path, items_key, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {items_key: []}
    client = RedirectRuleApiClient(https)
    list(getattr(client, method_name)(*args))
    https.get.assert_called_with(expected_path)


def test_redirect_rule_api_client_get(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"redirect_rule": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.redirect_rule_api_client.to_domain", return_value=mocker.Mock()
    )
    client = RedirectRuleApiClient(https)
    client.get("abc123")
    https.get.assert_called_with("/api/v2/guide/redirect_rules/abc123")


def test_redirect_rule_api_client_create(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"redirect_rule": {}}
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.redirect_rule_api_client.to_domain", return_value=mocker.Mock()
    )
    mocker.patch(
        "libzapi.infrastructure.api_clients.help_center.redirect_rule_api_client.to_payload_create",
        return_value={"redirect_rule": {"redirect_from": "/old"}},
    )
    client = RedirectRuleApiClient(https)
    client.create(mocker.Mock())
    https.post.assert_called_with("/api/v2/guide/redirect_rules", json={"redirect_rule": {"redirect_from": "/old"}})


def test_redirect_rule_api_client_delete(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = RedirectRuleApiClient(https)
    client.delete("abc123")
    https.delete.assert_called_with("/api/v2/guide/redirect_rules/abc123")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_redirect_rule_api_client_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = RedirectRuleApiClient(https)
    with pytest.raises(error_cls):
        client.get("1")
