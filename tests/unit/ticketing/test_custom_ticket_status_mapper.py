from libzapi.application.commands.ticketing.custom_ticket_status_cmds import (
    CreateCustomTicketStatusCmd,
    UpdateCustomTicketStatusCmd,
)
from libzapi.infrastructure.mappers.ticketing.custom_ticket_status_mapper import (
    to_payload_create,
    to_payload_update,
)


def test_create_minimum_payload():
    payload = to_payload_create(
        CreateCustomTicketStatusCmd(status_category="open", agent_label="In Progress")
    )
    assert payload == {
        "custom_status": {
            "status_category": "open",
            "agent_label": "In Progress",
        }
    }


def test_create_with_all_fields():
    payload = to_payload_create(
        CreateCustomTicketStatusCmd(
            status_category="open",
            agent_label="In Progress",
            end_user_label="Being worked",
            description="agent desc",
            end_user_description="eu desc",
            active=True,
        )
    )
    assert payload == {
        "custom_status": {
            "status_category": "open",
            "agent_label": "In Progress",
            "end_user_label": "Being worked",
            "description": "agent desc",
            "end_user_description": "eu desc",
            "active": True,
        }
    }


def test_create_preserves_false_active():
    payload = to_payload_create(
        CreateCustomTicketStatusCmd(
            status_category="open", agent_label="x", active=False
        )
    )
    assert payload["custom_status"]["active"] is False


def test_create_omits_none_fields():
    payload = to_payload_create(
        CreateCustomTicketStatusCmd(
            status_category="open",
            agent_label="x",
            end_user_label=None,
            description=None,
            active=None,
        )
    )
    body = payload["custom_status"]
    assert "end_user_label" not in body
    assert "description" not in body
    assert "active" not in body


def test_update_empty_returns_empty_body():
    payload = to_payload_update(UpdateCustomTicketStatusCmd())
    assert payload == {"custom_status": {}}


def test_update_with_agent_label():
    payload = to_payload_update(UpdateCustomTicketStatusCmd(agent_label="New"))
    assert payload == {"custom_status": {"agent_label": "New"}}


def test_update_with_all_fields():
    payload = to_payload_update(
        UpdateCustomTicketStatusCmd(
            agent_label="a",
            end_user_label="b",
            description="c",
            end_user_description="d",
            active=False,
        )
    )
    assert payload == {
        "custom_status": {
            "agent_label": "a",
            "end_user_label": "b",
            "description": "c",
            "end_user_description": "d",
            "active": False,
        }
    }


def test_update_preserves_false_active():
    payload = to_payload_update(UpdateCustomTicketStatusCmd(active=False))
    assert payload["custom_status"]["active"] is False
