import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.switchboard import SwitchboardIntegration
from libzapi.infrastructure.api_clients.conversations.switchboard_integration_api_client import (
    SwitchboardIntegrationApiClient,
)

MODULE = "libzapi.infrastructure.api_clients.conversations.switchboard_integration_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(SwitchboardIntegration, id=just("sbi-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "switchboard_integration:sbi-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"switchboardIntegrations": [{}]}

    client = SwitchboardIntegrationApiClient(https)
    list(client.list_all("app-1", "sb-1"))

    https.get_raw.assert_called_with(
        "https://example.zendesk.com/sc/v2/apps/app-1/switchboards/sb-1/switchboardIntegrations?page[size]=100"
    )


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create_switchboard_integration", return_value={"name": "bot"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"switchboardIntegration": {}}

    client = SwitchboardIntegrationApiClient(https)
    client.create("app-1", "sb-1", mocker.Mock())

    https.post.assert_called_with(
        "/v2/apps/app-1/switchboards/sb-1/switchboardIntegrations",
        {"name": "bot"},
    )


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update_switchboard_integration", return_value={"name": "updated"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.patch.return_value = {"switchboardIntegration": {}}

    client = SwitchboardIntegrationApiClient(https)
    client.update("app-1", "sb-1", "sbi-1", mocker.Mock())

    https.patch.assert_called_with(
        "/v2/apps/app-1/switchboards/sb-1/switchboardIntegrations/sbi-1",
        {"name": "updated"},
    )


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = SwitchboardIntegrationApiClient(https)
    client.delete("app-1", "sb-1", "sbi-1")

    https.delete.assert_called_with("/v2/apps/app-1/switchboards/sb-1/switchboardIntegrations/sbi-1")


# ── error propagation: list_all (get) ──────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_all_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.side_effect = error_cls("error")

    client = SwitchboardIntegrationApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1", "sb-1"))


# ── error propagation: create (post) ──────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_create_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_create_switchboard_integration", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = SwitchboardIntegrationApiClient(https)

    with pytest.raises(error_cls):
        client.create("app-1", "sb-1", mocker.Mock())


# ── error propagation: delete ──────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_delete_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.delete.side_effect = error_cls("error")

    client = SwitchboardIntegrationApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "sb-1", "sbi-1")
