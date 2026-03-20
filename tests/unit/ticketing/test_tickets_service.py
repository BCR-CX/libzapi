import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_cmds import CreateTicketCmd, UpdateTicketCmd
from libzapi.application.services.ticketing.tickets_service import TickestService
from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.domain.models.ticketing.ticket import CustomField


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(client=None):
    client = client or Mock()
    return TickestService(client), client


# ---------------------------------------------------------------------------
# create
# ---------------------------------------------------------------------------


class TestCreate:
    def test_delegates_to_client_with_create_ticket_cmd(self):
        service, client = _make_service()
        client.create_ticket.return_value = sentinel.ticket

        result = service.create(subject="Help me", description="Something broke")

        client.create_ticket.assert_called_once()
        cmd = client.create_ticket.call_args.kwargs["entity"]
        assert isinstance(cmd, CreateTicketCmd)
        assert cmd.subject == "Help me"
        assert cmd.description == "Something broke"
        assert result is sentinel.ticket

    def test_converts_custom_field_dicts_to_domain_objects(self):
        service, client = _make_service()
        raw_fields = [
            {"id": 100, "value": "alpha"},
            {"id": 200, "value": "beta"},
        ]

        service.create(subject="s", description="d", custom_fields=raw_fields)

        cmd = client.create_ticket.call_args.kwargs["entity"]
        assert cmd.custom_fields == [
            CustomField(id=100, value="alpha"),
            CustomField(id=200, value="beta"),
        ]

    def test_passes_all_optional_fields(self):
        service, client = _make_service()

        service.create(
            subject="s",
            description="d",
            tags=("urgent", "billing"),
            priority="high",
            ticket_type="incident",
            group_id=10,
            requester_id=20,
            organization_id=30,
            problem_id=40,
            ticket_form_id=50,
            brand_id=60,
        )

        cmd = client.create_ticket.call_args.kwargs["entity"]
        assert cmd.tags == ("urgent", "billing")
        assert cmd.priority == "high"
        assert cmd.type == "incident"
        assert cmd.group_id == 10
        assert cmd.requester_id == 20
        assert cmd.organization_id == 30
        assert cmd.problem_id == 40
        assert cmd.ticket_form_id == 50
        assert cmd.brand_id == 60

    def test_defaults_produce_empty_collections_and_none_ids(self):
        service, client = _make_service()

        service.create(subject="s", description="d")

        cmd = client.create_ticket.call_args.kwargs["entity"]
        assert cmd.custom_fields == []
        assert cmd.tags == ()
        assert cmd.priority == ""
        assert cmd.type == ""
        assert cmd.group_id is None
        assert cmd.requester_id is None
        assert cmd.organization_id is None
        assert cmd.problem_id is None
        assert cmd.ticket_form_id is None
        assert cmd.brand_id is None


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------


class TestUpdate:
    def test_delegates_to_client_with_update_ticket_cmd(self):
        service, client = _make_service()
        client.update_ticket.return_value = sentinel.updated

        result = service.update(ticket_id=42, subject="New subject")

        client.update_ticket.assert_called_once()
        assert client.update_ticket.call_args.kwargs["ticket_id"] == 42
        cmd = client.update_ticket.call_args.kwargs["entity"]
        assert isinstance(cmd, UpdateTicketCmd)
        assert cmd.subject == "New subject"
        assert result is sentinel.updated

    def test_converts_custom_field_dicts_to_domain_objects(self):
        service, client = _make_service()

        service.update(
            ticket_id=1,
            custom_fields=[{"id": 300, "value": "gamma"}],
        )

        cmd = client.update_ticket.call_args.kwargs["entity"]
        assert cmd.custom_fields == [CustomField(id=300, value="gamma")]

    def test_passes_all_optional_fields(self):
        service, client = _make_service()

        service.update(
            ticket_id=1,
            subject="s",
            description="d",
            tags=("vip",),
            priority="low",
            ticket_type="task",
            group_id=11,
            requester_id=21,
            organization_id=31,
            problem_id=41,
            ticket_form_id=51,
            brand_id=61,
        )

        cmd = client.update_ticket.call_args.kwargs["entity"]
        assert cmd.subject == "s"
        assert cmd.description == "d"
        assert cmd.tags == ("vip",)
        assert cmd.priority == "low"
        assert cmd.type == "task"
        assert cmd.group_id == 11
        assert cmd.requester_id == 21
        assert cmd.organization_id == 31
        assert cmd.problem_id == 41
        assert cmd.ticket_form_id == 51
        assert cmd.brand_id == 61


# ---------------------------------------------------------------------------
# create_many
# ---------------------------------------------------------------------------


class TestCreateMany:
    def test_converts_list_of_dicts_to_create_commands(self):
        service, client = _make_service()
        client.create_many.return_value = sentinel.many

        items = [
            {"subject": "Ticket A", "description": "Desc A"},
            {"subject": "Ticket B", "description": "Desc B", "priority": "urgent", "type": "problem"},
        ]

        result = service.create_many(items)

        client.create_many.assert_called_once()
        cmds = client.create_many.call_args.kwargs["entity"]
        assert len(cmds) == 2
        assert all(isinstance(c, CreateTicketCmd) for c in cmds)
        assert cmds[0].subject == "Ticket A"
        assert cmds[0].description == "Desc A"
        assert cmds[0].priority == ""
        assert cmds[1].priority == "urgent"
        assert cmds[1].type == "problem"
        assert result is sentinel.many

    def test_converts_custom_fields_inside_each_dict(self):
        service, client = _make_service()
        items = [
            {
                "subject": "s",
                "description": "d",
                "custom_fields": [{"id": 1, "value": "x"}, {"id": 2, "value": "y"}],
            },
        ]

        service.create_many(items)

        cmd = client.create_many.call_args.kwargs["entity"][0]
        assert cmd.custom_fields == [
            CustomField(id=1, value="x"),
            CustomField(id=2, value="y"),
        ]

    def test_missing_optional_keys_use_defaults(self):
        service, client = _make_service()
        items = [{"subject": "s", "description": "d"}]

        service.create_many(items)

        cmd = client.create_many.call_args.kwargs["entity"][0]
        assert cmd.custom_fields == []
        assert cmd.tags == ()
        assert cmd.priority == ""
        assert cmd.type == ""
        assert cmd.group_id is None
        assert cmd.brand_id is None

    def test_empty_input_calls_client_with_empty_list(self):
        service, client = _make_service()

        service.create_many([])

        client.create_many.assert_called_once_with(entity=[])


# ---------------------------------------------------------------------------
# Delegation-only methods
# ---------------------------------------------------------------------------


class TestDelegation:
    def test_list_delegates(self):
        service, client = _make_service()
        client.list.return_value = sentinel.tickets

        assert service.list() is sentinel.tickets
        client.list.assert_called_once()

    def test_get_delegates(self):
        service, client = _make_service()
        client.get.return_value = sentinel.ticket

        assert service.get(ticket_id=99) is sentinel.ticket
        client.get.assert_called_once_with(ticket_id=99)

    def test_list_organization_delegates(self):
        service, client = _make_service()
        service.list_organization(organization_id=5)
        client.list_organization.assert_called_once_with(organization_id=5)

    def test_list_user_requested_delegates(self):
        service, client = _make_service()
        service.list_user_requested(user_id=7)
        client.list_user_requested.assert_called_once_with(user_id=7)

    def test_count_delegates(self):
        service, client = _make_service()
        client.count.return_value = sentinel.count
        assert service.count() is sentinel.count

    def test_show_multiple_tickets_delegates(self):
        service, client = _make_service()
        service.show_multiple_tickets(ticket_ids=[1, 2, 3])
        client.show_multiple_tickets.assert_called_once_with(ticket_ids=[1, 2, 3])


# ---------------------------------------------------------------------------
# Error propagation
# ---------------------------------------------------------------------------


class TestErrorPropagation:
    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_create_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create_ticket.side_effect = error_cls("boom")

        with pytest.raises(error_cls):
            service.create(subject="s", description="d")

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound, UnprocessableEntity, RateLimited])
    def test_update_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.update_ticket.side_effect = error_cls("boom")

        with pytest.raises(error_cls):
            service.update(ticket_id=1, subject="s")

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_list_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.list.side_effect = error_cls("boom")

        with pytest.raises(error_cls):
            service.list()

    @pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
    def test_create_many_propagates_client_error(self, error_cls):
        service, client = _make_service()
        client.create_many.side_effect = error_cls("boom")

        with pytest.raises(error_cls):
            service.create_many([{"subject": "s", "description": "d"}])


# ---------------------------------------------------------------------------
# cast_to_ticket_command (static helper)
# ---------------------------------------------------------------------------


class TestCastToTicketCommand:
    def test_creates_create_ticket_cmd(self):
        cmd = TickestService.cast_to_ticket_command(
            CreateTicketCmd,
            brand_id=1,
            description="d",
            fields=[CustomField(id=10, value="v")],
            group_id=2,
            organization_id=3,
            priority="high",
            problem_id=4,
            requester_id=5,
            subject="s",
            tags=("t",),
            ticket_form_id=6,
            ticket_type="task",
        )
        assert isinstance(cmd, CreateTicketCmd)
        assert cmd.brand_id == 1
        assert cmd.custom_fields == [CustomField(id=10, value="v")]

    def test_creates_update_ticket_cmd(self):
        cmd = TickestService.cast_to_ticket_command(
            UpdateTicketCmd,
            brand_id=None,
            description=None,
            fields=[],
            group_id=None,
            organization_id=None,
            priority="",
            problem_id=None,
            requester_id=None,
            subject=None,
            tags=(),
            ticket_form_id=None,
            ticket_type="",
        )
        assert isinstance(cmd, UpdateTicketCmd)
        assert cmd.subject is None
        assert cmd.description is None
