from libzapi.application.commands.ticketing.ticket_skip_cmds import CreateTicketSkipCmd
from libzapi.infrastructure.mappers.ticketing.ticket_skip_mapper import to_payload_create


def test_create_payload():
    payload = to_payload_create(CreateTicketSkipCmd(reason="not my area"))
    assert payload == {"skip": {"reason": "not my area"}}


def test_create_empty_reason():
    payload = to_payload_create(CreateTicketSkipCmd(reason=""))
    assert payload == {"skip": {"reason": ""}}
