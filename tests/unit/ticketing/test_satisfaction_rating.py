import pytest

from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.ticketing import SatisfactionRatingApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.satisfaction_rating_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


def test_list_no_filters_hits_base_path(http, domain):
    http.get.return_value = {"satisfaction_ratings": []}
    client = SatisfactionRatingApiClient(http)
    list(client.list())
    http.get.assert_called_with("/api/v2/satisfaction_ratings")


def test_list_with_score_encodes_query(http, domain):
    http.get.return_value = {"satisfaction_ratings": []}
    client = SatisfactionRatingApiClient(http)
    list(client.list(score="bad"))
    http.get.assert_called_with("/api/v2/satisfaction_ratings?score=bad")


def test_list_with_time_window(http, domain):
    http.get.return_value = {"satisfaction_ratings": []}
    client = SatisfactionRatingApiClient(http)
    list(client.list(start_time=100, end_time=200))
    http.get.assert_called_with(
        "/api/v2/satisfaction_ratings?start_time=100&end_time=200"
    )


def test_list_yields_items(http, domain):
    http.get.return_value = {
        "satisfaction_ratings": [{"id": 1}, {"id": 2}],
        "meta": {"has_more": False},
        "links": {"next": None},
    }
    client = SatisfactionRatingApiClient(http)
    assert len(list(client.list())) == 2


def test_list_received(http, domain):
    http.get.return_value = {"satisfaction_ratings": [{"id": 1}]}
    client = SatisfactionRatingApiClient(http)
    assert len(list(client.list_received())) == 1
    http.get.assert_called_with("/api/v2/satisfaction_ratings/received")


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------


def test_get_calls_endpoint(http, domain):
    http.get.return_value = {"satisfaction_rating": {"id": 5}}
    client = SatisfactionRatingApiClient(http)
    client.get(rating_id=5)
    http.get.assert_called_with("/api/v2/satisfaction_ratings/5")


# ---------------------------------------------------------------------------
# create_for_ticket
# ---------------------------------------------------------------------------


def test_create_for_ticket_posts_payload(http, domain):
    http.post.return_value = {"satisfaction_rating": {"id": 1}}
    client = SatisfactionRatingApiClient(http)
    client.create_for_ticket(
        ticket_id=42,
        entity=CreateSatisfactionRatingCmd(score="good", comment="nice"),
    )
    http.post.assert_called_with(
        "/api/v2/tickets/42/satisfaction_rating",
        {"satisfaction_rating": {"score": "good", "comment": "nice"}},
    )


# ---------------------------------------------------------------------------
# reasons
# ---------------------------------------------------------------------------


def test_list_reasons(http, domain):
    http.get.return_value = {"reasons": [{"id": 1}, {"id": 2}]}
    client = SatisfactionRatingApiClient(http)
    assert len(list(client.list_reasons())) == 2
    http.get.assert_called_with("/api/v2/satisfaction_reasons")


def test_get_reason_calls_endpoint(http, domain):
    http.get.return_value = {"reason": {"id": 5}}
    client = SatisfactionRatingApiClient(http)
    client.get_reason(reason_id=5)
    http.get.assert_called_with("/api/v2/satisfaction_reasons/5")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited]
)
def test_raises_on_http_error(error_cls, http):
    http.get.side_effect = error_cls("error")
    client = SatisfactionRatingApiClient(http)
    with pytest.raises(error_cls):
        list(client.list())


# ---------------------------------------------------------------------------
# Domain logical keys
# ---------------------------------------------------------------------------


def test_satisfaction_rating_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.satisfaction_rating import SatisfactionRating

    r = SatisfactionRating(
        id=1,
        score="good",
        ticket_id=42,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert r.logical_key.as_str() == "satisfaction_rating:rating_id_1"


def test_satisfaction_reason_logical_key():
    from datetime import datetime

    from libzapi.domain.models.ticketing.satisfaction_rating import SatisfactionReason

    r = SatisfactionReason(
        id=9,
        reason_code=100,
        raw_reason={"value": "too slow"},
        reason={"value": "too slow"},
        value="too slow",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert r.logical_key.as_str() == "satisfaction_reason:reason_id_9"
