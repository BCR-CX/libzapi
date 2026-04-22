from libzapi.application.commands.ticketing.satisfaction_rating_cmds import (
    CreateSatisfactionRatingCmd,
)
from libzapi.infrastructure.mappers.ticketing.satisfaction_rating_mapper import (
    to_payload_create,
)


def test_create_minimum_payload():
    payload = to_payload_create(CreateSatisfactionRatingCmd(score="good"))
    assert payload == {"satisfaction_rating": {"score": "good"}}


def test_create_with_comment():
    payload = to_payload_create(
        CreateSatisfactionRatingCmd(score="bad", comment="not great")
    )
    assert payload == {
        "satisfaction_rating": {"score": "bad", "comment": "not great"}
    }


def test_create_with_reason_id():
    payload = to_payload_create(
        CreateSatisfactionRatingCmd(score="bad", reason_id=7)
    )
    assert payload == {
        "satisfaction_rating": {"score": "bad", "reason_id": 7}
    }


def test_create_full_payload():
    payload = to_payload_create(
        CreateSatisfactionRatingCmd(score="bad", comment="too slow", reason_id=9)
    )
    assert payload == {
        "satisfaction_rating": {
            "score": "bad",
            "comment": "too slow",
            "reason_id": 9,
        }
    }


def test_create_empty_comment_is_preserved():
    payload = to_payload_create(
        CreateSatisfactionRatingCmd(score="good", comment="")
    )
    assert payload["satisfaction_rating"]["comment"] == ""


def test_create_coerces_reason_id_to_int():
    payload = to_payload_create(
        CreateSatisfactionRatingCmd(score="bad", reason_id="5")  # type: ignore[arg-type]
    )
    assert isinstance(payload["satisfaction_rating"]["reason_id"], int)
    assert payload["satisfaction_rating"]["reason_id"] == 5
