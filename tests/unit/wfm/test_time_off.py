import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.application.commands.wfm.time_off_cmds import ImportTimeOffCmd, ImportTimeOffEntry
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.wfm.time_off import TimeOff
from libzapi.infrastructure.api_clients.wfm import TimeOffApiClient

MODULE = "libzapi.infrastructure.api_clients.wfm.time_off_api_client"

strategy = builds(
    TimeOff,
    timeOffRequestId=just("req-1"),
    agentId=just(1),
    startTime=just(100),
    endTime=just(200),
)


@given(strategy)
def test_logical_key(model: TimeOff):
    assert model.logical_key.as_str() == "wfm_time_off:req-1"


def test_list_calls_correct_path_no_filters(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{}]}
    client = TimeOffApiClient(https)
    list(client.list())
    https.get.assert_called_with("/wfm/public/api/v1/timeOff")


def test_list_with_filters(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{}]}
    client = TimeOffApiClient(https)
    list(client.list(agent_id=42, status="approved", page=1, per_page=25))
    https.get.assert_called_with("/wfm/public/api/v1/timeOff?agentId=42&status=approved&page=1&perPage=25")


def test_list_empty(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": []}
    client = TimeOffApiClient(https)
    assert list(client.list()) == []


def test_import_time_off(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    mocker.patch(
        f"{MODULE}.to_payload_import",
        return_value={"data": [{"agentId": 1, "startTime": 100, "endTime": 200, "reasonId": "r1"}]},
    )
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.post.return_value = {"success": True, "data": {"entities": [], "inserted": [], "updated": []}}
    client = TimeOffApiClient(https)
    cmd = ImportTimeOffCmd(data=[ImportTimeOffEntry(agentId=1, startTime=100, endTime=200, reasonId="r1")])
    client.import_time_off(cmd=cmd)
    https.post.assert_called_with(
        "/wfm/public/api/v1/timeOff/import",
        json={"data": [{"agentId": 1, "startTime": 100, "endTime": 200, "reasonId": "r1"}]},
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
def test_list_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = TimeOffApiClient(https)
    with pytest.raises(error_cls):
        list(client.list())


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_import_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.post.side_effect = error_cls("error")
    client = TimeOffApiClient(https)
    cmd = ImportTimeOffCmd(data=[ImportTimeOffEntry(agentId=1, startTime=100, endTime=200, reasonId="r1")])
    with pytest.raises(error_cls):
        client.import_time_off(cmd=cmd)
