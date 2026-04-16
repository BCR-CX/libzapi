import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.application.commands.wfm.shift_cmds import FetchShiftsCmd
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.wfm.shift import Shift
from libzapi.infrastructure.api_clients.wfm import ShiftApiClient

MODULE = "libzapi.infrastructure.api_clients.wfm.shift_api_client"

strategy = builds(Shift, id=just("shift-1"), agentId=just(1), startTime=just(100), endTime=just(200))


@given(strategy)
def test_logical_key(model: Shift):
    assert model.logical_key.as_str() == "wfm_shift:shift-1"


def test_fetch_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(
        f"{MODULE}.to_payload_fetch",
        return_value={"startDate": "2024-01-01", "endDate": "2024-01-31"},
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"data": [{}]}
    client = ShiftApiClient(https)
    cmd = FetchShiftsCmd(startDate="2024-01-01", endDate="2024-01-31")
    list(client.fetch(cmd=cmd))
    https.post.assert_called_with(
        "/wfm/public/api/v1/shifts/fetch",
        json={"startDate": "2024-01-01", "endDate": "2024-01-31"},
    )


def test_fetch_empty(mocker):
    mocker.patch(f"{MODULE}.to_payload_fetch", return_value={})
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"data": []}
    client = ShiftApiClient(https)
    cmd = FetchShiftsCmd(startDate="2024-01-01", endDate="2024-01-31")
    assert list(client.fetch(cmd=cmd)) == []


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_fetch_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.post.side_effect = error_cls("error")
    client = ShiftApiClient(https)
    cmd = FetchShiftsCmd(startDate="2024-01-01", endDate="2024-01-31")
    with pytest.raises(error_cls):
        list(client.fetch(cmd=cmd))
