from __future__ import annotations

import libzapi.infrastructure.api_clients.conversations as api
from libzapi.application.services.conversations.activities_service import ActivitiesService
from libzapi.application.services.conversations.app_keys_service import AppKeysService
from libzapi.application.services.conversations.apps_service import AppsService
from libzapi.application.services.conversations.attachments_service import AttachmentsService
from libzapi.application.services.conversations.clients_service import ClientsService
from libzapi.application.services.conversations.conversations_service import ConversationsService
from libzapi.application.services.conversations.devices_service import DevicesService
from libzapi.application.services.conversations.integration_api_keys_service import IntegrationApiKeysService
from libzapi.application.services.conversations.integrations_service import IntegrationsService
from libzapi.application.services.conversations.messages_service import MessagesService
from libzapi.application.services.conversations.participants_service import ParticipantsService
from libzapi.application.services.conversations.switchboard_actions_service import SwitchboardActionsService
from libzapi.application.services.conversations.switchboard_integrations_service import SwitchboardIntegrationsService
from libzapi.application.services.conversations.switchboards_service import SwitchboardsService
from libzapi.application.services.conversations.users_service import UsersService
from libzapi.application.services.conversations.webhooks_service import WebhooksService
from libzapi.infrastructure.http.auth import basic_key_headers
from libzapi.infrastructure.http.client import HttpClient


class Conversations:
    def __init__(self, base_url: str, key_id: str, key_secret: str, app_id: str):
        headers = basic_key_headers(key_id, key_secret)
        http = HttpClient(f"{base_url.rstrip('/')}/sc", headers=headers)
        self.app_id = app_id

        self.apps = AppsService(api.AppApiClient(http))
        self.app_keys = AppKeysService(api.AppKeyApiClient(http), app_id)
        self.conversations_ = ConversationsService(api.ConversationApiClient(http), app_id)
        self.messages = MessagesService(api.MessageApiClient(http), app_id)
        self.participants = ParticipantsService(api.ParticipantApiClient(http), app_id)
        self.activities = ActivitiesService(api.ActivityApiClient(http), app_id)
        self.switchboard_actions = SwitchboardActionsService(api.SwitchboardActionApiClient(http), app_id)
        self.integrations = IntegrationsService(api.IntegrationApiClient(http), app_id)
        self.integration_api_keys = IntegrationApiKeysService(api.IntegrationApiKeyApiClient(http), app_id)
        self.webhooks = WebhooksService(api.WebhookApiClient(http), app_id)
        self.switchboards = SwitchboardsService(api.SwitchboardApiClient(http), app_id)
        self.switchboard_integrations = SwitchboardIntegrationsService(
            api.SwitchboardIntegrationApiClient(http), app_id
        )
        self.users = UsersService(api.UserApiClient(http), app_id)
        self.clients = ClientsService(api.ClientApiClient(http), app_id)
        self.devices = DevicesService(api.DeviceApiClient(http), app_id)
        self.attachments = AttachmentsService(api.AttachmentApiClient(http), app_id)
