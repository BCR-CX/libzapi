from libzapi.application.commands.ticketing.sla_policy_cmds import (
    CreateSlaPolicyCmd,
    UpdateSlaPolicyCmd,
)
from libzapi.infrastructure.mappers.ticketing.sla_policy_mapper import (
    to_payload_create,
    to_payload_update,
)


_FILTER = {"all": [], "any": []}
_METRICS = [
    {
        "priority": "low",
        "metric": "first_reply_time",
        "target": 480,
        "business_hours": False,
    }
]


def test_create_minimal_payload_only_includes_required():
    payload = to_payload_create(
        CreateSlaPolicyCmd(
            title="T", filter=_FILTER, policy_metrics=_METRICS
        )
    )
    assert payload == {
        "sla_policy": {
            "title": "T",
            "filter": _FILTER,
            "policy_metrics": _METRICS,
        }
    }


def test_create_includes_all_optional_fields():
    body = to_payload_create(
        CreateSlaPolicyCmd(
            title="T",
            filter=_FILTER,
            policy_metrics=_METRICS,
            description="d",
            position=3,
        )
    )["sla_policy"]
    assert body["description"] == "d"
    assert body["position"] == 3


def test_create_skips_none_optional_fields():
    body = to_payload_create(
        CreateSlaPolicyCmd(title="T", filter=_FILTER, policy_metrics=_METRICS)
    )["sla_policy"]
    assert "description" not in body
    assert "position" not in body


def test_create_converts_metrics_iterable_to_list():
    body = to_payload_create(
        CreateSlaPolicyCmd(
            title="T", filter=_FILTER, policy_metrics=iter(_METRICS)
        )
    )["sla_policy"]
    assert body["policy_metrics"] == _METRICS


def test_update_empty_cmd_returns_empty_patch():
    assert to_payload_update(UpdateSlaPolicyCmd()) == {"sla_policy": {}}


def test_update_includes_all_fields():
    body = to_payload_update(
        UpdateSlaPolicyCmd(
            title="New",
            filter=_FILTER,
            policy_metrics=_METRICS,
            description="d",
            position=5,
        )
    )["sla_policy"]
    assert body == {
        "title": "New",
        "filter": _FILTER,
        "policy_metrics": _METRICS,
        "description": "d",
        "position": 5,
    }


def test_update_converts_metrics_iterable_to_list():
    body = to_payload_update(
        UpdateSlaPolicyCmd(policy_metrics=iter(_METRICS))
    )["sla_policy"]
    assert body["policy_metrics"] == _METRICS
