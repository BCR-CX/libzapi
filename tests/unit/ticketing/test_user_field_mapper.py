from libzapi.application.commands.ticketing.user_field_cmds import (
    CreateUserFieldCmd,
    UpdateUserFieldCmd,
    UserFieldOptionCmd,
)
from libzapi.infrastructure.mappers.ticketing.user_field_mapper import (
    option_to_payload,
    to_payload_create,
    to_payload_update,
)


# ---------------------------------------------------------------------------
# to_payload_create
# ---------------------------------------------------------------------------


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateUserFieldCmd(key="region", type="text", title="Region")
    )
    assert payload == {
        "user_field": {"key": "region", "type": "text", "title": "Region"}
    }


def test_create_includes_all_optional_fields():
    cmd = CreateUserFieldCmd(
        key="region",
        type="tagger",
        title="Region",
        description="desc",
        active=True,
        position=3,
        regexp_for_validation=r"\d+",
        tag="r",
        relationship_target_type="zen:user",
        relationship_filter={"all": []},
        custom_field_options=[{"name": "A", "value": "a"}],
    )

    body = to_payload_create(cmd)["user_field"]

    assert body["key"] == "region"
    assert body["type"] == "tagger"
    assert body["title"] == "Region"
    assert body["description"] == "desc"
    assert body["active"] is True
    assert body["position"] == 3
    assert body["regexp_for_validation"] == r"\d+"
    assert body["tag"] == "r"
    assert body["relationship_target_type"] == "zen:user"
    assert body["relationship_filter"] == {"all": []}
    assert body["custom_field_options"] == [{"name": "A", "value": "a"}]


def test_create_preserves_false_booleans():
    body = to_payload_create(
        CreateUserFieldCmd(key="k", type="text", title="T", active=False)
    )["user_field"]
    assert body["active"] is False


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateUserFieldCmd(key="k", type="text", title="T")
    )["user_field"]
    assert set(body.keys()) == {"key", "type", "title"}


def test_create_converts_options_iterable_to_list():
    opts = [{"name": "A", "value": "a"}]
    body = to_payload_create(
        CreateUserFieldCmd(
            key="k", type="tagger", title="T", custom_field_options=iter(opts)
        )
    )["user_field"]
    assert body["custom_field_options"] == opts


# ---------------------------------------------------------------------------
# to_payload_update
# ---------------------------------------------------------------------------


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateUserFieldCmd()) == {"user_field": {}}


def test_update_includes_all_fields():
    cmd = UpdateUserFieldCmd(
        key="region",
        title="Region",
        description="d",
        active=True,
        position=1,
        regexp_for_validation=r"\d+",
        tag="r",
        relationship_target_type="zen:user",
        relationship_filter={"all": []},
        custom_field_options=[{"name": "A", "value": "a"}],
    )
    body = to_payload_update(cmd)["user_field"]
    assert body == {
        "key": "region",
        "title": "Region",
        "description": "d",
        "active": True,
        "position": 1,
        "regexp_for_validation": r"\d+",
        "tag": "r",
        "relationship_target_type": "zen:user",
        "relationship_filter": {"all": []},
        "custom_field_options": [{"name": "A", "value": "a"}],
    }


def test_update_preserves_false_booleans():
    body = to_payload_update(UpdateUserFieldCmd(active=False))["user_field"]
    assert body == {"active": False}


def test_update_converts_options_iterable_to_list():
    opts = [{"name": "A", "value": "a"}]
    body = to_payload_update(
        UpdateUserFieldCmd(custom_field_options=iter(opts))
    )["user_field"]
    assert body["custom_field_options"] == opts


# ---------------------------------------------------------------------------
# option_to_payload
# ---------------------------------------------------------------------------


def test_option_to_payload_without_id():
    payload = option_to_payload(UserFieldOptionCmd(name="A", value="a"))
    assert payload == {"custom_field_option": {"name": "A", "value": "a"}}


def test_option_to_payload_with_id():
    payload = option_to_payload(UserFieldOptionCmd(name="A", value="a", id=7))
    assert payload == {
        "custom_field_option": {"name": "A", "value": "a", "id": 7}
    }
