import pytest
from unittest.mock import Mock, sentinel

from libzapi.application.commands.ticketing.ticket_cmds import (
    CreateTicketCmd,
    MergeTicketsCmd,
    UpdateTicketCmd,
)
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


# ---------------------------------------------------------------------------
# New list/read methods (delegation)
# ---------------------------------------------------------------------------


class TestAdditionalListMethods:
    @pytest.mark.parametrize(
        "method, kwargs",
        [
            ("list_user_ccd", {"user_id": 7}),
            ("list_user_followed", {"user_id": 7}),
            ("list_user_assigned", {"user_id": 7}),
            ("list_recent", {}),
            ("list_collaborators", {"ticket_id": 11}),
            ("list_followers", {"ticket_id": 11}),
            ("list_email_ccs", {"ticket_id": 11}),
            ("list_incidents", {"ticket_id": 11}),
            ("list_problems", {}),
            ("organization_count", {"organization_id": 5}),
            ("user_ccd_count", {"user_id": 7}),
            ("user_assigned_count", {"user_id": 7}),
            ("list_related", {"ticket_id": 11}),
            ("list_deleted", {}),
        ],
    )
    def test_delegates_to_client(self, method, kwargs):
        service, client = _make_service()
        getattr(client, method).return_value = sentinel.result

        result = getattr(service, method)(**kwargs)

        getattr(client, method).assert_called_once_with(**kwargs)
        assert result is sentinel.result


# ---------------------------------------------------------------------------
# update_many / update_many_individually
# ---------------------------------------------------------------------------


class TestUpdateMany:
    def test_builds_update_cmd_and_delegates(self):
        service, client = _make_service()
        client.update_many.return_value = sentinel.job

        result = service.update_many([1, 2], priority="low", subject="s")

        client.update_many.assert_called_once()
        assert client.update_many.call_args.kwargs["ticket_ids"] == [1, 2]
        entity = client.update_many.call_args.kwargs["entity"]
        assert isinstance(entity, UpdateTicketCmd)
        assert entity.priority == "low"
        assert entity.subject == "s"
        assert result is sentinel.job

    def test_no_fields_yields_blank_cmd(self):
        service, client = _make_service()
        service.update_many([1])
        entity = client.update_many.call_args.kwargs["entity"]
        assert entity.priority is None
        assert entity.subject is None


class TestUpdateManyIndividually:
    def test_pairs_ids_with_update_cmds(self):
        service, client = _make_service()
        client.update_many_individually.return_value = sentinel.job

        result = service.update_many_individually(
            [(1, {"priority": "low"}), (2, {"tags": ["x"]})]
        )

        pairs = client.update_many_individually.call_args.kwargs["updates"]
        assert pairs[0][0] == 1
        assert isinstance(pairs[0][1], UpdateTicketCmd)
        assert pairs[0][1].priority == "low"
        assert pairs[1][0] == 2
        assert pairs[1][1].tags == ["x"]
        assert result is sentinel.job

    def test_empty_updates(self):
        service, client = _make_service()
        service.update_many_individually([])
        assert client.update_many_individually.call_args.kwargs["updates"] == []


# ---------------------------------------------------------------------------
# delete / destroy_many / spam / merge / restore / permanently_delete
# ---------------------------------------------------------------------------


class TestDestructive:
    def test_delete_delegates(self):
        service, client = _make_service()
        service.delete(ticket_id=5)
        client.delete.assert_called_once_with(ticket_id=5)

    def test_destroy_many_delegates(self):
        service, client = _make_service()
        client.destroy_many.return_value = sentinel.job
        assert service.destroy_many([1, 2]) is sentinel.job
        client.destroy_many.assert_called_once_with(ticket_ids=[1, 2])

    def test_mark_as_spam_delegates(self):
        service, client = _make_service()
        service.mark_as_spam(ticket_id=9)
        client.mark_as_spam.assert_called_once_with(ticket_id=9)

    def test_mark_many_as_spam_delegates(self):
        service, client = _make_service()
        client.mark_many_as_spam.return_value = sentinel.job
        assert service.mark_many_as_spam([1, 2]) is sentinel.job
        client.mark_many_as_spam.assert_called_once_with(ticket_ids=[1, 2])

    def test_restore_delegates(self):
        service, client = _make_service()
        service.restore(ticket_id=5)
        client.restore.assert_called_once_with(ticket_id=5)

    def test_restore_many_delegates(self):
        service, client = _make_service()
        service.restore_many([1, 2])
        client.restore_many.assert_called_once_with(ticket_ids=[1, 2])

    def test_permanently_delete_delegates(self):
        service, client = _make_service()
        client.permanently_delete.return_value = sentinel.job
        assert service.permanently_delete(ticket_id=5) is sentinel.job

    def test_permanently_delete_many_delegates(self):
        service, client = _make_service()
        client.permanently_delete_many.return_value = sentinel.job
        assert service.permanently_delete_many([1, 2]) is sentinel.job


class TestMerge:
    def test_builds_merge_cmd_with_defaults(self):
        service, client = _make_service()
        client.merge.return_value = sentinel.job

        result = service.merge(target_ticket_id=10, source_ids=[1, 2])

        entity = client.merge.call_args.kwargs["entity"]
        assert isinstance(entity, MergeTicketsCmd)
        assert entity.source_ids == [1, 2]
        assert entity.target_comment is None
        assert entity.source_comment is None
        assert entity.target_comment_is_public is False
        assert entity.source_comment_is_public is False
        assert client.merge.call_args.kwargs["target_ticket_id"] == 10
        assert result is sentinel.job

    def test_passes_comment_visibility_flags(self):
        service, client = _make_service()

        service.merge(
            target_ticket_id=10,
            source_ids=[1],
            target_comment="merged",
            source_comment="dup",
            target_comment_is_public=True,
            source_comment_is_public=True,
        )

        entity = client.merge.call_args.kwargs["entity"]
        assert entity.target_comment == "merged"
        assert entity.source_comment == "dup"
        assert entity.target_comment_is_public is True
        assert entity.source_comment_is_public is True


# ---------------------------------------------------------------------------
# problems_autocomplete + tag helpers
# ---------------------------------------------------------------------------


class TestAuxiliary:
    def test_problems_autocomplete_delegates(self):
        service, client = _make_service()
        client.problems_autocomplete.return_value = sentinel.matches
        assert service.problems_autocomplete(text="net") is sentinel.matches
        client.problems_autocomplete.assert_called_once_with(text="net")

    def test_list_tags_delegates(self):
        service, client = _make_service()
        client.list_tags.return_value = ["a", "b"]
        assert service.list_tags(ticket_id=5) == ["a", "b"]
        client.list_tags.assert_called_once_with(ticket_id=5)

    def test_set_tags_delegates(self):
        service, client = _make_service()
        client.set_tags.return_value = ["a"]
        assert service.set_tags(ticket_id=5, tags=["a"]) == ["a"]
        client.set_tags.assert_called_once_with(ticket_id=5, tags=["a"])

    def test_add_tags_delegates(self):
        service, client = _make_service()
        client.add_tags.return_value = ["a", "b"]
        assert service.add_tags(ticket_id=5, tags=["b"]) == ["a", "b"]
        client.add_tags.assert_called_once_with(ticket_id=5, tags=["b"])

    def test_remove_tags_delegates(self):
        service, client = _make_service()
        client.remove_tags.return_value = ["a"]
        assert service.remove_tags(ticket_id=5, tags=["b"]) == ["a"]
        client.remove_tags.assert_called_once_with(ticket_id=5, tags=["b"])
