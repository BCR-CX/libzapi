from libzapi.application.commands.ticketing.bookmark_cmds import CreateBookmarkCmd
from libzapi.infrastructure.mappers.ticketing.bookmark_mapper import to_payload_create


def test_create_payload():
    assert to_payload_create(CreateBookmarkCmd(ticket_id=42)) == {
        "bookmark": {"ticket_id": 42}
    }


def test_create_coerces_ticket_id():
    assert to_payload_create(CreateBookmarkCmd(ticket_id="7")) == {  # type: ignore[arg-type]
        "bookmark": {"ticket_id": 7}
    }
