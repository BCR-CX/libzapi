import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.integration import Integration
from libzapi.infrastructure.api_clients.conversations.integration_api_client import IntegrationApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.integration_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Integration, id=just("int-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "sunco_integration:int-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get_raw.return_value = {"integrations": [{}]}

    client = IntegrationApiClient(https)
    list(client.list_all("app-1"))

    https.get_raw.assert_called_with("https://example.zendesk.com/sc/v2/apps/app-1/integrations?page[size]=100")


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"integration": {}}

    client = IntegrationApiClient(https)
    client.get("app-1", "int-1")

    https.get.assert_called_with("/v2/apps/app-1/integrations/int-1")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create", return_value={"type": "web"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"integration": {}}

    client = IntegrationApiClient(https)
    client.create("app-1", mocker.Mock())

    https.post.assert_called_with("/v2/apps/app-1/integrations", {"type": "web"})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"displayName": "Updated"})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.patch.return_value = {"integration": {}}

    client = IntegrationApiClient(https)
    client.update("app-1", "int-1", mocker.Mock())

    https.patch.assert_called_with("/v2/apps/app-1/integrations/int-1", {"displayName": "Updated"})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = IntegrationApiClient(https)
    client.delete("app-1", "int-1")

    https.delete.assert_called_with("/v2/apps/app-1/integrations/int-1")


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

    client = IntegrationApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1"))


# ── error propagation: get ─────────────────────────────────────────────


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.side_effect = error_cls("error")

    client = IntegrationApiClient(https)

    with pytest.raises(error_cls):
        client.get("app-1", "int-1")


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
    mocker.patch(f"{MODULE}.to_payload_create", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = IntegrationApiClient(https)

    with pytest.raises(error_cls):
        client.create("app-1", mocker.Mock())


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

    client = IntegrationApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "int-1")
