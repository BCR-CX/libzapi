import pytest

from libzapi.domain.errors import NotFound, RateLimited, Unauthorized, UnprocessableEntity
from libzapi.infrastructure.api_clients.status.status_api_client import StatusApiClient


MODULE = "libzapi.infrastructure.api_clients.status.status_api_client"

ACTIVE_RESPONSE = {
    "data": [
        {
            "id": "inc-1",
            "type": "incident",
            "attributes": {
                "title": "API Degradation",
                "impact": "minor",
                "started_at": "2024-01-01T00:00:00Z",
                "status": "investigating",
                "outage": False,
                "degradation": True,
            },
            "relationships": {
                "incident_updates": {"data": [{"id": "upd-1", "type": "incident_update"}]},
            },
        }
    ],
    "included": [
        {
            "id": "upd-1",
            "type": "incident_update",
            "attributes": {"description": "We are investigating.", "created_at": "2024-01-01T00:01:00Z"},
        },
        {
            "id": "isvc-1",
            "type": "incident_service",
            "attributes": {"incident_id": "inc-1", "service_id": "svc-1", "outage": False, "degradation": True},
        },
        {
            "id": "svc-1",
            "type": "service",
            "attributes": {"name": "API", "slug": "api"},
        },
    ],
}

SINGLE_RESPONSE = {
    "data": {
        "id": "inc-1",
        "type": "incident",
        "attributes": {"title": "API Degradation", "impact": "minor", "status": "investigating"},
        "relationships": {"incident_updates": {"data": []}},
    },
    "included": [],
}


# ── list_active ─────────────────────────────────────────────────────────


def test_list_active_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.return_value = ACTIVE_RESPONSE

    client = StatusApiClient(https)
    list(client.list_active())

    https.get.assert_called_with("/api/incidents/active")


def test_list_active_with_subdomain(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.return_value = ACTIVE_RESPONSE

    client = StatusApiClient(https)
    list(client.list_active(subdomain="mycompany"))

    https.get.assert_called_with("/api/incidents/active?subdomain=mycompany")


# ── list_maintenance ────────────────────────────────────────────────────


def test_list_maintenance_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.return_value = {"data": [], "included": []}

    client = StatusApiClient(https)
    list(client.list_maintenance())

    https.get.assert_called_with("/api/incidents/maintenance")


def test_list_maintenance_with_subdomain(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.return_value = {"data": [], "included": []}

    client = StatusApiClient(https)
    list(client.list_maintenance(subdomain="mycompany"))

    https.get.assert_called_with("/api/incidents/maintenance?subdomain=mycompany")


# ── get ─────────────────────────────────────────────────────────────────


def test_get_calls_correct_path(mocker):
    mocker.patch(f"{MODULE}.to_domain", return_value=mocker.Mock())
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.return_value = SINGLE_RESPONSE

    client = StatusApiClient(https)
    client.get("inc-1")

    https.get.assert_called_with(
        "/api/incidents/inc-1?include[]=incident_updates&include[]=incident_services&include[]=incident_services.service"
    )


# ── error propagation ──────────────────────────────────────────────────


ERROR_CLASSES = [
    pytest.param(Unauthorized, id="401"),
    pytest.param(NotFound, id="404"),
    pytest.param(UnprocessableEntity, id="422"),
    pytest.param(RateLimited, id="429"),
]


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_list_active_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = StatusApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_active())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_list_maintenance_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = StatusApiClient(https)

    with pytest.raises(error_cls):
        list(client.list_maintenance())


@pytest.mark.parametrize("error_cls", ERROR_CLASSES)
def test_get_raises_on_http_error(error_cls, mocker):
    https = mocker.Mock()
    https.base_url = "https://status.zendesk.com"
    https.get.side_effect = error_cls("error")

    client = StatusApiClient(https)

    with pytest.raises(error_cls):
        client.get("inc-1")
