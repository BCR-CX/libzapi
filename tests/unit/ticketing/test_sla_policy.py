import pytest
from hypothesis import given
from hypothesis.strategies import just, builds

from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.sla_policies import SlaPolicy
from libzapi.infrastructure.api_clients.ticketing import SlaPolicyApiClient


strategy = builds(
    SlaPolicy,
    title=just("Sample"),
)


@given(strategy)
def test_session_logical_key_from_id(model: SlaPolicy):
    assert model.logical_key.as_str() == "sla_policy:sample"


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.sla_policy_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


_FILTER = {"all": [], "any": []}
_METRICS = [
    {
        "priority": "low",
        "metric": "first_reply_time",
        "target": 480,
        "business_hours": False,
    }
]


# ---------------------------------------------------------------------------
# Listing / pagination
# ---------------------------------------------------------------------------


def test_list_endpoint(mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.return_value = {"sla_policies": []}
    client = SlaPolicyApiClient(https)
    list(client.list())
    https.get.assert_called_with("/api/v2/slas/policies")


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "sla_policies": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = SlaPolicyApiClient(http)
    assert len(list(client.list())) == 2


# ---------------------------------------------------------------------------
# Simple endpoints
# ---------------------------------------------------------------------------


def test_list_definitions_returns_dict(http):
    http.get.return_value = {"definitions": {}}
    client = SlaPolicyApiClient(http)
    assert client.list_definitions() == {"definitions": {}}
    http.get.assert_called_with("/api/v2/slas/policies/definitions")


def test_get_returns_domain(http, domain):
    http.get.return_value = {"sla_policy": {"id": 5}}
    client = SlaPolicyApiClient(http)
    result = client.get(sla_policy_id=5)
    http.get.assert_called_with("/api/v2/slas/policies/5")
    assert result["id"] == 5


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------


def test_create_posts_payload(http, domain):
    http.post.return_value = {"sla_policy": {"id": 1}}
    client = SlaPolicyApiClient(http)
    client.create(
        CreateSlaPolicyCmd(
            title="T", filter=_FILTER, policy_metrics=_METRICS
        )
    )
    http.post.assert_called_with(
        "/api/v2/slas/policies",
        {
            "sla_policy": {
                "title": "T",
                "filter": _FILTER,
                "policy_metrics": _METRICS,
            }
        },
    )


def test_update_puts_payload(http, domain):
    http.put.return_value = {"sla_policy": {"id": 1, "description": "d"}}
    client = SlaPolicyApiClient(http)
    client.update(sla_policy_id=1, entity=UpdateSlaPolicyCmd(description="d"))
    http.put.assert_called_with(
        "/api/v2/slas/policies/1", {"sla_policy": {"description": "d"}}
    )


def test_delete_calls_delete(http):
    client = SlaPolicyApiClient(http)
    client.delete(sla_policy_id=7)
    http.delete.assert_called_with("/api/v2/slas/policies/7")


# ---------------------------------------------------------------------------
# Reorder
# ---------------------------------------------------------------------------


def test_reorder_puts_ids(http, domain):
    http.put.return_value = {
        "sla_policies": [{"id": 1}, {"id": 2}]
    }
    client = SlaPolicyApiClient(http)
    result = client.reorder([2, 1])
    http.put.assert_called_with(
        "/api/v2/slas/policies/reorder", {"sla_policy_ids": [2, 1]}
    )
    assert len(result) == 2


def test_reorder_handles_missing_key(http, domain):
    http.put.return_value = {}
    client = SlaPolicyApiClient(http)
    assert client.reorder([1]) == []


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls",
    [
        pytest.param(Unauthorized, id="401"),
        pytest.param(NotFound, id="404"),
        pytest.param(UnprocessableEntity, id="422"),
        pytest.param(RateLimited, id="429"),
    ],
)
def test_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://example.zendesk.com"
    https.get.side_effect = error_cls("error")
    client = SlaPolicyApiClient(https)
    with pytest.raises(error_cls):
        list(client.list())
