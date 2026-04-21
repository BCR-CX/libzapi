from libzapi.application.commands.ticketing.request_cmds import (
    CreateRequestCmd,
    UpdateRequestCmd,
)
from libzapi.infrastructure.mappers.ticketing.request_mapper import (
    to_payload_create,
    to_payload_update,
)


def test_create_minimal_payload():
    payload = to_payload_create(
        CreateRequestCmd(subject="S", comment={"body": "hi"})
    )
    assert payload == {
        "request": {"subject": "S", "comment": {"body": "hi"}}
    }


def test_create_includes_all_fields():
    payload = to_payload_create(
        CreateRequestCmd(
            subject="S",
            comment={"body": "hi"},
            requester={"name": "A", "email": "a@x"},
            priority="high",
            type="question",
            custom_fields=[{"id": 1, "value": "v"}],
            ticket_form_id=9,
            recipient="r@x",
            collaborators=[1, 2],
            email_ccs=[{"user_id": 3}],
            due_at="2030-01-01T00:00Z",
        )
    )
    body = payload["request"]
    assert body["subject"] == "S"
    assert body["requester"] == {"name": "A", "email": "a@x"}
    assert body["priority"] == "high"
    assert body["type"] == "question"
    assert body["custom_fields"] == [{"id": 1, "value": "v"}]
    assert body["ticket_form_id"] == 9
    assert body["recipient"] == "r@x"
    assert body["collaborators"] == [1, 2]
    assert body["email_ccs"] == [{"user_id": 3}]
    assert body["due_at"] == "2030-01-01T00:00Z"


def test_create_converts_custom_fields_iterable():
    payload = to_payload_create(
        CreateRequestCmd(
            subject="S",
            comment={"body": "hi"},
            custom_fields=iter([{"id": 1, "value": "v"}]),
        )
    )
    assert payload["request"]["custom_fields"] == [{"id": 1, "value": "v"}]


def test_create_converts_collaborators_iterable():
    payload = to_payload_create(
        CreateRequestCmd(
            subject="S", comment={"body": "hi"}, collaborators=iter([1])
        )
    )
    assert payload["request"]["collaborators"] == [1]


def test_update_empty_patch():
    assert to_payload_update(UpdateRequestCmd()) == {"request": {}}


def test_update_includes_all_fields():
    payload = to_payload_update(
        UpdateRequestCmd(
            comment={"body": "hi", "public": True},
            solved=True,
            additional_collaborators=[5],
            email_ccs=[{"user_id": 3}],
        )
    )
    assert payload == {
        "request": {
            "comment": {"body": "hi", "public": True},
            "solved": True,
            "additional_collaborators": [5],
            "email_ccs": [{"user_id": 3}],
        }
    }


def test_update_preserves_false_solved():
    payload = to_payload_update(UpdateRequestCmd(solved=False))
    assert payload["request"]["solved"] is False


def test_update_converts_iterables():
    payload = to_payload_update(
        UpdateRequestCmd(
            additional_collaborators=iter([1]),
            email_ccs=iter([{"user_id": 2}]),
        )
    )
    assert payload["request"]["additional_collaborators"] == [1]
    assert payload["request"]["email_ccs"] == [{"user_id": 2}]
