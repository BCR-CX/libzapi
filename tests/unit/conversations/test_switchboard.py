import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.conversations.switchboard import Switchboard
from libzapi.infrastructure.api_clients.conversations.switchboard_api_client import SwitchboardApiClient

MODULE = "libzapi.infrastructure.api_clients.conversations.switchboard_api_client"

# ── Hypothesis ──────────────────────────────────────────────────────────

strategy = builds(Switchboard, id=just("sb-1"))


@given(strategy)
def test_logical_key(model):
    assert model.logical_key.as_str() == "switchboard:sb-1"


# ── list_all ────────────────────────────────────────────────────────────


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.get.return_value = {"switchboards": [{}]}

    client = SwitchboardApiClient(https)
    list(client.list_all("app-1"))

    https.get.assert_called_with("/v2/apps/app-1/switchboards")


# ── create ──────────────────────────────────────────────────────────────


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create_switchboard", return_value={"enabled": True})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.return_value = {"switchboard": {}}

    client = SwitchboardApiClient(https)
    client.create("app-1", mocker.Mock())

    https.post.assert_called_with("/v2/apps/app-1/switchboards", {"enabled": True})


# ── update ──────────────────────────────────────────────────────────────


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update_switchboard", return_value={"enabled": False})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.patch.return_value = {"switchboard": {}}

    client = SwitchboardApiClient(https)
    client.update("app-1", "sb-1", mocker.Mock())

    https.patch.assert_called_with("/v2/apps/app-1/switchboards/sb-1", {"enabled": False})


# ── delete ──────────────────────────────────────────────────────────────


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"

    client = SwitchboardApiClient(https)
    client.delete("app-1", "sb-1")

    https.delete.assert_called_with("/v2/apps/app-1/switchboards/sb-1")


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
    https.get.side_effect = error_cls("error")

    client = SwitchboardApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_all("app-1"))


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
    mocker.patch(f"{MODULE}.to_payload_create_switchboard", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com/sc"
    https.post.side_effect = error_cls("error")

    client = SwitchboardApiClient(https)

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

    client = SwitchboardApiClient(https)

    with pytest.raises(error_cls):
        client.delete("app-1", "sb-1")
