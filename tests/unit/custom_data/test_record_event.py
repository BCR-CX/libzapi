import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.custom_data.record_event import RecordEvent
from libzapi.infrastructure.api_clients.custom_data.record_event import RecordEventApiClient

MODULE = "libzapi.infrastructure.api_clients.custom_data.record_event"

strategy = builds(RecordEvent, id=just("evt-1"), type=just("record_created"))


@given(strategy)
def test_logical_key(model: RecordEvent):
    assert model.logical_key.as_str() == "record_event:evt-1"


def test_list_all_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"events": [{}], "meta": {"has_more": False}, "links": [{"next": ""}]}
    client = RecordEventApiClient(https)
    list(client.list_all("car", "rec-1", page_size=50))
    https.get.assert_called_with("/api/v2/custom_objects/car/records/rec-1/events?page[size]=50")


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
    https.get.side_effect = error_cls("error")
    client = RecordEventApiClient(https)
    with pytest.raises(error_cls):
        list(client.list_all("car", "rec-1"))
