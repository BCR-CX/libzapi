import pytest

from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.infrastructure.api_clients.ticketing import JobStatusApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.job_status_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_list_yields_job_statuses(http, domain):
    http.get.return_value = {
        "job_statuses": [{"id": "a"}, {"id": "b"}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = JobStatusApiClient(http)
    items = list(client.list())
    http.get.assert_called_with("/api/v2/job_statuses")
    assert len(items) == 2


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"job_status": {"id": "abc"}}
    client = JobStatusApiClient(http)
    client.get("abc")
    http.get.assert_called_with("/api/v2/job_statuses/abc")


def test_show_many_builds_path(http, domain):
    http.get.return_value = {"job_statuses": [{"id": "a"}, {"id": "b"}]}
    client = JobStatusApiClient(http)
    result = client.show_many(["a", "b"])
    http.get.assert_called_with("/api/v2/job_statuses/show_many?ids=a,b")
    assert len(result) == 2


def test_show_many_handles_missing_key(http, domain):
    http.get.return_value = {}
    client = JobStatusApiClient(http)
    assert client.show_many(["a"]) == []


def test_show_many_handles_null(http, domain):
    http.get.return_value = {"job_statuses": None}
    client = JobStatusApiClient(http)
    assert client.show_many(["a"]) == []


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_get_propagates_error(error_cls, http):
    http.get.side_effect = error_cls("boom")
    client = JobStatusApiClient(http)
    with pytest.raises(error_cls):
        client.get("abc")
