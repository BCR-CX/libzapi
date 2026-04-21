from libzapi.application.commands.ticketing.ticket_cmds import (
    CreateTicketCmd,
    MergeTicketsCmd,
    UpdateTicketCmd,
)
from libzapi.domain.models.ticketing.ticket import CustomField
from libzapi.infrastructure.mappers.ticketing.ticket_mapper import (
    to_payload_create,
    to_payload_merge,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_includes_all_fields():
    cmd = CreateTicketCmd(
        subject="s",
        description="d",
        custom_fields=[CustomField(id=1, value="v")],
        priority="high",
        type="incident",
        group_id=10,
        requester_id=20,
        organization_id=30,
        problem_id=40,
        tags=["a"],
        ticket_form_id=50,
        brand_id=60,
    )

    payload = to_payload_create(cmd)["ticket"]

    assert payload["subject"] == "s"
    assert payload["description"] == "d"
    assert payload["custom_fields"] == [{"id": 1, "value": "v"}]
    assert payload["priority"] == "high"
    assert payload["type"] == "incident"
    assert payload["group_id"] == 10
    assert payload["requester_id"] == 20
    assert payload["organization_id"] == 30
    assert payload["problem_id"] == 40
    assert payload["tags"] == ["a"]
    assert payload["ticket_form_id"] == 50
    assert payload["brand_id"] == 60


def test_create_with_empty_custom_fields():
    cmd = CreateTicketCmd(subject="s", description="d", custom_fields=[])
    payload = to_payload_create(cmd)["ticket"]
    assert payload["custom_fields"] == []


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateTicketCmd()) == {"ticket": {}}


def test_update_only_includes_truthy_fields():
    cmd = UpdateTicketCmd(
        subject="s",
        custom_fields=[CustomField(id=1, value="v")],
        description="d",
        priority="low",
        type="task",
        group_id=1,
        requester_id=2,
        organization_id=3,
        problem_id=4,
        tags=["x"],
        ticket_form_id=5,
        brand_id=6,
    )
    payload = to_payload_update(cmd)["ticket"]
    assert payload == {
        "subject": "s",
        "custom_fields": [{"id": 1, "value": "v"}],
        "description": "d",
        "priority": "low",
        "type": "task",
        "group_id": 1,
        "requester_id": 2,
        "organization_id": 3,
        "problem_id": 4,
        "tags": ["x"],
        "ticket_form_id": 5,
        "brand_id": 6,
    }


def test_update_skips_empty_strings_and_none():
    cmd = UpdateTicketCmd(subject="", description=None, priority="", tags=[])
    assert to_payload_update(cmd) == {"ticket": {}}


# ---------------------------------------------------------------------------
# to_payload_merge
# ---------------------------------------------------------------------------


def test_merge_without_comments_yields_only_ids():
    cmd = MergeTicketsCmd(source_ids=[1, 2, 3])
    assert to_payload_merge(cmd) == {"ids": [1, 2, 3]}


def test_merge_with_target_comment_includes_visibility_flag():
    cmd = MergeTicketsCmd(source_ids=[1], target_comment="hi", target_comment_is_public=True)
    payload = to_payload_merge(cmd)
    assert payload["target_comment"] == "hi"
    assert payload["target_comment_is_public"] is True
    assert "source_comment" not in payload


def test_merge_with_source_comment_includes_visibility_flag():
    cmd = MergeTicketsCmd(
        source_ids=[1],
        source_comment="dup",
        source_comment_is_public=False,
    )
    payload = to_payload_merge(cmd)
    assert payload["source_comment"] == "dup"
    assert payload["source_comment_is_public"] is False
    assert "target_comment" not in payload


def test_merge_accepts_iterable_source_ids():
    cmd = MergeTicketsCmd(source_ids=iter([4, 5]))
    payload = to_payload_merge(cmd)
    assert payload["ids"] == [4, 5]
