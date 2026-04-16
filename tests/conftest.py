import os
from typing import Type, TypeVar

import pytest

from libzapi import Ticketing, HelpCenter, CustomData, AgentAvailability, AssetManagement, Conversations, Voice, WorkforceManagement

T = TypeVar("T")


@pytest.fixture(scope="session")
def ticketing():
    """Creates a real Ticketing client if environment variables are set."""
    return _generic_zendesk_client(Ticketing)


@pytest.fixture(scope="session")
def custom_data():
    """Creates a real Help Center client if environment variables are set."""
    return _generic_zendesk_client(CustomData)


@pytest.fixture(scope="session")
def help_center():
    """Creates a real Help Center client if environment variables are set."""
    return _generic_zendesk_client(HelpCenter)


@pytest.fixture(scope="session")
def agent_availability():
    """Creates a real Agent Availability client if environment variables are set."""
    return _generic_zendesk_client(AgentAvailability)


@pytest.fixture(scope="session")
def asset_management():
    """Creates a real Asset Management client if environment variables are set."""
    return _generic_zendesk_client(AssetManagement)


@pytest.fixture(scope="session")
def conversations():
    """Creates a real Conversations client if environment variables are set."""
    base_url = os.getenv("ZENDESK_URL")
    key_id = os.getenv("SUNCO_KEY_ID")
    key_secret = os.getenv("SUNCO_KEY_SECRET")
    app_id = os.getenv("SUNCO_APP_ID")

    if not (base_url and key_id and key_secret and app_id):
        pytest.skip("Sunshine Conversations credentials not provided. Skipping live API tests.")

    return Conversations(base_url=base_url, key_id=key_id, key_secret=key_secret, app_id=app_id)


@pytest.fixture(scope="session")
def voice():
    """Creates a real Voice client if environment variables are set."""
    return _generic_zendesk_client(Voice)


@pytest.fixture(scope="session")
def wfm():
    """Creates a real WorkforceManagement client if environment variables are set."""
    return _generic_zendesk_client(WorkforceManagement)


def _generic_zendesk_client(client_cls: Type[T]) -> T:
    base_url = os.getenv("ZENDESK_URL")
    email = os.getenv("ZENDESK_EMAIL")
    api_token = os.getenv("ZENDESK_TOKEN")

    if not (base_url and email and api_token):
        pytest.skip("Zendesk credentials not provided. Skipping live API tests.")

    return client_cls(
        base_url=base_url,
        email=email,
        api_token=api_token,
    )
