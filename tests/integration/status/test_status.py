import pytest

from libzapi import ZendeskStatus


@pytest.fixture(scope="session")
def zendesk_status():
    return ZendeskStatus()


def test_list_active_incidents(zendesk_status: ZendeskStatus):
    incidents = list(zendesk_status.incidents.list_active())
    assert isinstance(incidents, list)


def test_list_maintenance_incidents(zendesk_status: ZendeskStatus):
    incidents = list(zendesk_status.incidents.list_maintenance())
    assert isinstance(incidents, list)


def test_get_active_incident(zendesk_status: ZendeskStatus):
    incidents = list(zendesk_status.incidents.list_active())
    if not incidents:
        pytest.skip("No active incidents to fetch")
    incident = zendesk_status.incidents.get(incidents[0].id)
    assert incident.id == incidents[0].id
