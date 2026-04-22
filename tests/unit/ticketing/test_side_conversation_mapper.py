from libzapi.application.commands.ticketing.side_conversation_cmds import (
    CreateSideConversationCmd,
    ReplySideConversationCmd,
    SideConversationMessageCmd,
    UpdateSideConversationCmd,
)
from libzapi.infrastructure.mappers.ticketing.side_conversation_mapper import (
    to_payload_create,
    to_payload_reply,
    to_payload_update,
)


def test_create_minimal():
    payload = to_payload_create(
        CreateSideConversationCmd(
            message=SideConversationMessageCmd(body="hello"),
        )
    )
    assert payload == {"side_conversation": {"message": {"body": "hello"}}}


def test_create_with_subject_and_to():
    payload = to_payload_create(
        CreateSideConversationCmd(
            message=SideConversationMessageCmd(
                body="hi",
                subject="Question",
                to=[{"email": "x@example.com"}],
                from_={"support_address_id": 1},
                body_html="<p>hi</p>",
                attachment_ids=["a1", "a2"],
            ),
            external_ids={"foo": "bar"},
        )
    )
    assert payload == {
        "side_conversation": {
            "message": {
                "body": "hi",
                "subject": "Question",
                "to": [{"email": "x@example.com"}],
                "from": {"support_address_id": 1},
                "body_html": "<p>hi</p>",
                "attachment_ids": ["a1", "a2"],
            },
            "external_ids": {"foo": "bar"},
        }
    }


def test_reply_minimal():
    payload = to_payload_reply(
        ReplySideConversationCmd(message=SideConversationMessageCmd(body="reply"))
    )
    assert payload == {"message": {"body": "reply"}}


def test_reply_with_attachments():
    payload = to_payload_reply(
        ReplySideConversationCmd(
            message=SideConversationMessageCmd(
                body="r",
                body_html="<p>r</p>",
                attachment_ids=["a1"],
            )
        )
    )
    assert payload == {
        "message": {
            "body": "r",
            "body_html": "<p>r</p>",
            "attachment_ids": ["a1"],
        }
    }


def test_update_empty():
    payload = to_payload_update(UpdateSideConversationCmd())
    assert payload == {"side_conversation": {}}


def test_update_with_state():
    payload = to_payload_update(UpdateSideConversationCmd(state="closed"))
    assert payload == {"side_conversation": {"state": "closed"}}
