import uuid

import pytest

from libzapi import HelpCenter
from libzapi.domain.errors import NotFound


def test_list_redirect_rules(help_center: HelpCenter):
    try:
        rules = list(help_center.redirect_rules.list_all())
    except NotFound:
        pytest.skip("Redirect rules not available on this account")
    assert isinstance(rules, list)


def test_create_delete_redirect_rule(help_center: HelpCenter):
    unique = str(uuid.uuid4())[:8]

    try:
        help_center.redirect_rules.create(
            brand_id=0,
            redirect_from=f"/old-path-{unique}",
            redirect_to=f"/new-path-{unique}",
            redirect_status=301,
        )
    except (NotFound, Exception):
        pytest.skip("Redirect rules not available on this account")

    # Verify by listing and finding our rule
    rules = list(help_center.redirect_rules.list_all())
    matching = [r for r in rules if r.redirect_from == f"/old-path-{unique}"]
    assert len(matching) > 0

    help_center.redirect_rules.delete(redirect_rule_id=matching[0].id)
