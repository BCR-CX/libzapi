import pytest
from hypothesis import given
from hypothesis.strategies import builds, just

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.wfm.report import Grouping, ReportRow
from libzapi.infrastructure.api_clients.wfm import ReportApiClient

MODULE = "libzapi.infrastructure.api_clients.wfm.report_api_client"

strategy = builds(
    ReportRow,
    groupings=just([Grouping(key="agent", value="john")]),
    metrics=just([]),
)


@given(strategy)
def test_logical_key(model: ReportRow):
    assert model.logical_key.as_str() == "wfm_report_row:john"


def test_get_data_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": [{}]}
    client = ReportApiClient(https)
    list(client.get_data(template_id="tmpl-1", start_time=100, end_time=200))
    https.get.assert_called_with("/wfm/public/api/v1/reports/tmpl-1/data?startTime=100&endTime=200")


def test_get_data_empty(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"data": []}
    client = ReportApiClient(https)
    assert list(client.get_data(template_id="t", start_time=1, end_time=2)) == []


def test_get_data_with_relationships(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"success": True, "data": [], "relationships": {}}
    client = ReportApiClient(https)
    result = client.get_data_with_relationships(template_id="t", start_time=1, end_time=2)
    assert result["success"] is True


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_get_data_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.get.side_effect = error_cls("error")
    client = ReportApiClient(https)
    with pytest.raises(error_cls):
        list(client.get_data(template_id="t", start_time=1, end_time=2))
