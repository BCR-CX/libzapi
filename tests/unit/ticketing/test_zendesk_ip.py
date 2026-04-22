import pytest

from libzapi.domain.errors import NotFound, Unauthorized
from libzapi.domain.models.ticketing.zendesk_ip import ZendeskIPs
from libzapi.infrastructure.api_clients.ticketing import ZendeskIPApiClient


@pytest.fixture
def http(mocker):
    m = mocker.Mock()
    m.base_url = "https://example.zendesk.com"
    return m


@pytest.fixture
def domain(mocker):
    return mocker.patch(
        "libzapi.infrastructure.api_clients.ticketing.zendesk_ip_api_client.to_domain",
        side_effect=lambda data, cls: {"_cls": cls.__name__, **(data or {})},
    )


def test_get_calls_ips_endpoint(http, domain):
    http.get.return_value = {
        "project": "pod_eu_west_1",
        "egress_ips": ["1.1.1.1", "2.2.2.2"],
        "ingress_ips": ["3.3.3.3"],
        "app_id": "support",
    }
    client = ZendeskIPApiClient(http)
    result = client.get()
    http.get.assert_called_once_with("/api/v2/ips.json")
    domain.assert_called_once_with(
        data={
            "project": "pod_eu_west_1",
            "egress_ips": ["1.1.1.1", "2.2.2.2"],
            "ingress_ips": ["3.3.3.3"],
            "app_id": "support",
        },
        cls=ZendeskIPs,
    )
    assert result["_cls"] == "ZendeskIPs"
    assert result["project"] == "pod_eu_west_1"


def test_get_passes_empty_payload_to_domain(http, domain):
    http.get.return_value = {}
    client = ZendeskIPApiClient(http)
    result = client.get()
    domain.assert_called_once_with(data={}, cls=ZendeskIPs)
    assert result["_cls"] == "ZendeskIPs"


@pytest.mark.parametrize("error_cls", [Unauthorized, NotFound])
def test_get_propagates_error(error_cls, http):
    http.get.side_effect = error_cls("boom")
    client = ZendeskIPApiClient(http)
    with pytest.raises(error_cls):
        client.get()


def test_domain_dataclass_defaults():
    ips = ZendeskIPs()
    assert ips.project is None
    assert ips.egress_ips == []
    assert ips.ingress_ips == []
    assert ips.app_id is None


def test_domain_dataclass_is_frozen():
    ips = ZendeskIPs(project="pod_x")
    with pytest.raises(Exception):
        ips.project = "pod_y"  # type: ignore[misc]
