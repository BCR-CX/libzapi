from libzapi import HelpCenter


def test_list_permission_groups(help_center: HelpCenter):
    groups = list(help_center.permission_groups.list_all())
    assert len(groups) > 0, "Expected at least one permission group"


def test_create_get_update_delete_permission_group(help_center: HelpCenter):
    group = help_center.permission_groups.create(name="Integration Test PG")
    assert group.id is not None

    try:
        fetched = help_center.permission_groups.get(permission_group_id=group.id)
        assert fetched.id == group.id

        updated = help_center.permission_groups.update(
            permission_group_id=group.id,
            name="Updated Integration Test PG",
        )
        assert updated.name == "Updated Integration Test PG"
    finally:
        help_center.permission_groups.delete(permission_group_id=group.id)
