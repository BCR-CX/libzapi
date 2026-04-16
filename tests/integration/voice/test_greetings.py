import pytest
from libzapi import Voice


def test_list_greetings(voice: Voice):
    greetings = list(voice.greetings.list_all())
    assert isinstance(greetings, list)


def test_list_and_get_greeting(voice: Voice):
    greetings = list(voice.greetings.list_all())
    if not greetings:
        pytest.skip("No greetings found")
    greeting = voice.greetings.get(greetings[0].id)
    assert greeting.id == greetings[0].id


def test_list_greeting_categories(voice: Voice):
    categories = list(voice.greetings.list_categories())
    assert isinstance(categories, list)
    assert len(categories) > 0


def test_create_update_delete_greeting(voice: Voice):
    categories = list(voice.greetings.list_categories())
    if not categories:
        pytest.skip("No greeting categories found")
    greeting = voice.greetings.create(category_id=categories[0].id, name="Integration Test Greeting")
    assert greeting.id is not None
    try:
        updated = voice.greetings.update(greeting.id, name="Updated Test Greeting")
        assert updated.name == "Updated Test Greeting"
        fetched = voice.greetings.get(greeting.id)
        assert fetched.id == greeting.id
    finally:
        voice.greetings.delete(greeting.id)
