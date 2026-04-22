import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)
from libzapi.application.services.ticketing.satisfaction_ratings_service import (
    SatisfactionRatingsService,
)
from libzapi.domain.errors import NotFound, Unauthorized


def _make_service(client=None):
    client = client or Mock()
    return SatisfactionRatingsService(client), client


class TestList:
    def test_list_all_with_no_filters_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.ratings
        assert service.list_all() is sentinel.ratings
        client.list.assert_called_once_with(score=None, start_time=None, end_time=None)

    def test_list_all_with_filters(self):
        service, client = _make_service()
        service.list_all(score="bad", start_time=1, end_time=2)
        client.list.assert_called_once_with(score="bad", start_time=1, end_time=2)

    def test_list_received_delegates(self):
        service, client = _make_service()
        client.list_received.return_value = sentinel.ratings
        assert service.list_received() is sentinel.ratings
        client.list_received.assert_called_once_with()


class TestGet:
    def test_get_by_id_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.rating
        assert service.get_by_id(5) is sentinel.rating
        client.get.assert_called_once_with(rating_id=5)


class TestCreateForTicket:
    def test_builds_cmd_and_delegates(self):
        service, client = _make_service()
        client.create_for_ticket.return_value = sentinel.rating

        result = service.create_for_ticket(
            ticket_id=42, score="good", comment="nice"
        )

        call = client.create_for_ticket.call_args
        assert call.kwargs["ticket_id"] == 42
        cmd = call.kwargs["entity"]
        assert isinstance(cmd, CreateSatisfactionRatingCmd)
        assert cmd.score == "good"
        assert cmd.comment == "nice"
        assert cmd.reason_id is None
        assert result is sentinel.rating

    def test_forwards_reason_id(self):
        service, client = _make_service()
        service.create_for_ticket(ticket_id=1, score="bad", reason_id=7)
        cmd = client.create_for_ticket.call_args.kwargs["entity"]
        assert cmd.reason_id == 7


class TestReasons:
    def test_list_reasons_delegates(self):
        service, client = _make_service()
        client.list_reasons.return_value = sentinel.reasons
        assert service.list_reasons() is sentinel.reasons
        client.list_reasons.assert_called_once_with()

    def test_get_reason_delegates(self):
        service, client = _make_service()
        client.get_reason.return_value = sentinel.reason
        assert service.get_reason(9) is sentinel.reason
        client.get_reason.assert_called_once_with(reason_id=9)


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.list_all()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_propagates_error(self, error_cls):
        service, client = _make_service()
        client.create_for_ticket.side_effect = error_cls("boom")
        with pytest.raises(error_cls):
            service.create_for_ticket(ticket_id=1, score="good")
