import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.availability import Availability
from libzapi.infrastructure.api_clients.voice.availability_api_client import AvailabilityApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.availability_api_client"

strategy = builds(Availability, agent_state=just("online"))


@given(strategy)
def test_logical_key(model: Availability) -> None:
    assert model.logical_key.as_str() == "availability:online"


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"availability": {}}
    client = AvailabilityApiClient(https)
    client.get(42)
    https.get.assert_called_with("/api/v2/channels/voice/availabilities/42")


def test_update_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"availability": {"agent_state": "online"}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.return_value = {"availability": {}}
    client = AvailabilityApiClient(https)
    client.update(42, mocker.Mock())
    https.put.assert_called_with(
        "/api/v2/channels/voice/availabilities/42", json={"availability": {"agent_state": "online"}}
    )


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
    client = AvailabilityApiClient(https)
    with pytest.raises(error_cls):
        client.get(42)


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_update_raises_on_http_error(error_cls, mocker):
    mocker.patch(f"{MODULE}.to_payload_update", return_value={"availability": {}})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.put.side_effect = error_cls("error")
    client = AvailabilityApiClient(https)
    with pytest.raises(error_cls):
        client.update(42, mocker.Mock())
