import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.wfm.activity import Activity
from libzapi.infrastructure.api_clients.wfm import ActivityApiClient

MODULE = "libzapi.infrastructure.api_clients.wfm.activity_api_client"

strategy = builds(Activity, id=just("abc-123"), agentId=just(1), startTime=just(100), type=just("ticket"))


@given(strategy)
def test_logical_key(model: Activity):
    assert model.logical_key.as_str() == "wfm_activity:abc-123"


def test_list_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{}], "metadata": {}}
    client = ActivityApiClient(https)
    list(client.list(start_time=1706820299))
    https.get.assert_called_with("/wfm/public/api/v1/activities?startTime=1706820299")


def test_list_follows_pagination(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = [
        {"data": [{}], "metadata": {"next": "/wfm/public/api/v1/activities?startTime=999"}},
        {"data": [{}], "metadata": {}},
    ]
    client = ActivityApiClient(https)
    results = list(client.list(start_time=100))
    assert len(results) == 2
    assert https.get.call_count == 2


def test_list_handles_absolute_next_url(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = [
        {"data": [{}], "metadata": {"next": "https://example.zendesk.com/wfm/public/api/v1/activities?startTime=999"}},
        {"data": [], "metadata": {}},
    ]
    client = ActivityApiClient(https)
    list(client.list(start_time=100))
    https.get.assert_any_call("/wfm/public/api/v1/activities?startTime=999")


def test_list_with_relationships(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {
        "data": [{}],
        "relationships": {"agent": [{}], "activityType": [{}]},
    }
    client = ActivityApiClient(https)
    activities, agents, types = client.list_with_relationships(start_time=100)
    assert len(activities) == 1
    assert len(agents) == 1
    assert len(types) == 1


def test_list_empty_data(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [], "metadata": {}}
    client = ActivityApiClient(https)
    assert list(client.list(start_time=100)) == []


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
    client = ActivityApiClient(https)
    with pytest.raises(error_cls):
        list(client.list(start_time=100))


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_list_with_relationships_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = ActivityApiClient(https)
    with pytest.raises(error_cls):
        client.list_with_relationships(start_time=100)
