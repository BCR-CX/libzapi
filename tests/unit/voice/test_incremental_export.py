import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.voice.call import Call, CallLeg
from libzapi.infrastructure.api_clients.voice.incremental_export_api_client import IncrementalExportApiClient

MODULE = "libzapi.infrastructure.api_clients.voice.incremental_export_api_client"

call_strategy = builds(Call, id=just(1))
leg_strategy = builds(CallLeg, id=just(1))


@given(call_strategy)
def test_call_logical_key(model: Call) -> None:
    assert model.logical_key.as_str() == "call:1"


@given(leg_strategy)
def test_call_leg_logical_key(model: CallLeg) -> None:
    assert model.logical_key.as_str() == "call_leg:1"


def test_calls_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"calls": []}
    client = IncrementalExportApiClient(https)
    list(client.calls(start_time=100))
    https.get.assert_called_with("/api/v2/channels/voice/stats/incremental/calls?start_time=100")


def test_legs_calls_correct_path(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"legs": []}
    client = IncrementalExportApiClient(https)
    list(client.legs(start_time=100))
    https.get.assert_called_with("/api/v2/channels/voice/stats/incremental/legs?start_time=100")


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_calls_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = IncrementalExportApiClient(https)
    with pytest.raises(error_cls):
        list(client.calls(start_time=100))


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_legs_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = IncrementalExportApiClient(https)
    with pytest.raises(error_cls):
        list(client.legs(start_time=100))
