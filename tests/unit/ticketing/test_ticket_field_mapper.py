from libzapi.application.commands.ticketing.ticket_field_cmds import (
    CreateTicketFieldCmd,
    TicketFieldOptionCmd,
    UpdateTicketFieldCmd,
)
from libzapi.infrastructure.mappers.ticketing.ticket_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(CreateTicketFieldCmd(title="Order", type="text"))
    assert payload == {"ticket_field": {"title": "Order", "type": "text"}}


def test_create_includes_all_optional_fields():
    cmd = CreateTicketFieldCmd(
        title="Order",
        type="tagger",
        description="desc",
        active=True,
        required=True,
        collapsed_for_agents=True,
        regexp_for_validation=r"^\d+$",
        title_in_portal="Order #",
        visible_in_portal=True,
        editable_in_portal=True,
        required_in_portal=True,
        agent_can_edit=True,
        tag="order",
        position=3,
        custom_field_options=[{"name": "A", "value": "a"}],
        sub_type_id=2,
        relationship_target_type="zen:user",
        relationship_filter={"all": []},
        agent_description="internal",
    )

    body = to_payload_create(cmd)["ticket_field"]

    assert body["title"] == "Order"
    assert body["type"] == "tagger"
    assert body["description"] == "desc"
    assert body["active"] is True
    assert body["required"] is True
    assert body["collapsed_for_agents"] is True
    assert body["regexp_for_validation"] == r"^\d+$"
    assert body["title_in_portal"] == "Order #"
    assert body["visible_in_portal"] is True
    assert body["editable_in_portal"] is True
    assert body["required_in_portal"] is True
    assert body["agent_can_edit"] is True
    assert body["tag"] == "order"
    assert body["position"] == 3
    assert body["custom_field_options"] == [{"name": "A", "value": "a"}]
    assert body["sub_type_id"] == 2
    assert body["relationship_target_type"] == "zen:user"
    assert body["relationship_filter"] == {"all": []}
    assert body["agent_description"] == "internal"


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateTicketFieldCmd(
            title="t",
            type="text",
            active=False,
            required=False,
            collapsed_for_agents=False,
            visible_in_portal=False,
            editable_in_portal=False,
            required_in_portal=False,
            agent_can_edit=False,
        )
    )["ticket_field"]
    assert body["active"] is False
    assert body["required"] is False
    assert body["collapsed_for_agents"] is False
    assert body["visible_in_portal"] is False
    assert body["editable_in_portal"] is False
    assert body["required_in_portal"] is False
    assert body["agent_can_edit"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateTicketFieldCmd(title="t", type="text")
    )["ticket_field"]
    assert set(body.keys()) == {"title", "type"}


def test_create_converts_options_iterable_to_list():
    opts = [{"name": "A", "value": "a"}]
    body = to_payload_create(
        CreateTicketFieldCmd(
            title="t", type="tagger", custom_field_options=iter(opts)
        )
    )["ticket_field"]
    assert body["custom_field_options"] == opts


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateTicketFieldCmd()) == {"ticket_field": {}}


def test_update_includes_all_fields():
    cmd = UpdateTicketFieldCmd(
        title="New",
        description="d",
        active=True,
        required=True,
        collapsed_for_agents=True,
        regexp_for_validation=r"\d+",
        title_in_portal="Foo",
        visible_in_portal=True,
        editable_in_portal=True,
        required_in_portal=True,
        agent_can_edit=True,
        tag="x",
        position=1,
        custom_field_options=[{"name": "A", "value": "a"}],
        sub_type_id=9,
        relationship_target_type="zen:user",
        relationship_filter={"all": []},
        agent_description="hi",
    )
    body = to_payload_update(cmd)["ticket_field"]
    assert body == {
        "title": "New",
        "description": "d",
        "active": True,
        "required": True,
        "collapsed_for_agents": True,
        "regexp_for_validation": r"\d+",
        "title_in_portal": "Foo",
        "visible_in_portal": True,
        "editable_in_portal": True,
        "required_in_portal": True,
        "agent_can_edit": True,
        "tag": "x",
        "position": 1,
        "custom_field_options": [{"name": "A", "value": "a"}],
        "sub_type_id": 9,
        "relationship_target_type": "zen:user",
        "relationship_filter": {"all": []},
        "agent_description": "hi",
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateTicketFieldCmd(active=False))["ticket_field"]
    assert body == {"active": False}


def test_update_converts_options_iterable_to_list():
    opts = [{"name": "A", "value": "a"}]
    body = to_payload_update(
        UpdateTicketFieldCmd(custom_field_options=iter(opts))
    )["ticket_field"]
    assert body["custom_field_options"] == opts


# ---------------------------------------------------------------------------
# option_to_payload
# ---------------------------------------------------------------------------


def test_option_to_payload_without_id():
    payload = option_to_payload(TicketFieldOptionCmd(name="A", value="a"))
    assert payload == {"custom_field_option": {"name": "A", "value": "a"}}


def test_option_to_payload_with_id():
    payload = option_to_payload(TicketFieldOptionCmd(name="A", value="a", id=42))
    assert payload == {
        "custom_field_option": {"name": "A", "value": "a", "id": 42}
    }
