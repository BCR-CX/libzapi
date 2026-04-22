from libzapi import Ticketing
from libzapi.domain.models.ticketing.zendesk_ip import ZendeskIPs


def test_get_current_zendesk_ips(ticketing: Ticketing):
    ips = ticketing.zendesk_ips.get_current()
    assert isinstance(ips, ZendeskIPs)
    assert isinstance(ips.project, str) and ips.project
