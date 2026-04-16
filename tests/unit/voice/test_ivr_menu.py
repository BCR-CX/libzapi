import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.ivr import IvrMenu
from libzapi.infrastructure.api_clients.voice.ivr_menu_api_client import IvrMenuApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.ivr_menu_api_client"

strategy = builds(IvrMenu, id=just(1))


@given(strategy)
def test_logical_key(model: IvrMenu) -> None:
    assert model.logical_key.as_str() == "ivr_menu:1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"menus": [{}]}
    client = IvrMenuApiClient(https)
    list(client.list_all(1))
    https.get.assert_called_with("/api/v2/channels/voice/ivr/1/menus")


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"menu": {}}
    client = IvrMenuApiClient(https)
    client.get(1, 2)
    https.get.assert_called_with("/api/v2/channels/voice/ivr/1/menus/2")


def test_create_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_create_menu", return_value={"menu": {"name": "m"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"menu": {}}
    client = IvrMenuApiClient(https)
    client.create(1, mocker.Mock())
    https.post.assert_called_with("/api/v2/channels/voice/ivr/1/menus", json={"menu": {"name": "m"}})


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update_menu", return_value={"menu": {"name": "u"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"menu": {}}
    client = IvrMenuApiClient(https)
    client.update(1, 2, mocker.Mock())
    https.put.assert_called_with("/api/v2/channels/voice/ivr/1/menus/2", json={"menu": {"name": "u"}})


def test_delete_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    client = IvrMenuApiClient(https)
    client.delete(1, 2)
    https.delete.assert_called_with("/api/v2/channels/voice/ivr/1/menus/2")


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
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = IvrMenuApiClient(https)
    with pytest.raises(error_cls):
        client.get(1, 2)


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
    mocker.patch(f"{MODULE}.to_payload_create_menu", return_value={"menu": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.side_effect = error_cls("error")
    client = IvrMenuApiClient(https)
    with pytest.raises(error_cls):
        client.create(1, mocker.Mock())


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
    https.base_url = "https://example.zendesk.com"
    https.delete.side_effect = error_cls("error")
    client = IvrMenuApiClient(https)
    with pytest.raises(error_cls):
        client.delete(1, 2)
