from libzapi.application.services.custom_data.access_rules_service import AccessRulesService
from libzapi.application.services.custom_data.custom_object_fields_service import CustomObjectFieldsService
from libzapi.application.services.custom_data.custom_object_records import CustomObjectRecordsService
from libzapi.application.services.custom_data.custom_objects_service import CustomObjectsService
from libzapi.application.services.custom_data.object_triggers_service import ObjectTriggersService
from libzapi.application.services.custom_data.permission_policies_service import PermissionPoliciesService
from libzapi.application.services.custom_data.record_attachments_service import RecordAttachmentsService
from libzapi.application.services.custom_data.record_events_service import RecordEventsService
from libzapi.infrastructure.http.auth import api_token_headers, oauth_headers
from libzapi.infrastructure.http.client import HttpClient
import libzapi.infrastructure.api_clients.custom_data as api


class CustomData:
    def __init__(
        self, base_url: str, oauth_token: str | None = None, email: str | None = None, api_token: str | None = None
    ):
        if oauth_token:
            headers = oauth_headers(oauth_token)
        elif email and api_token:
            headers = api_token_headers(email, api_token)
        else:
            raise ValueError("Provide oauth_token or email+api_token")

        http = HttpClient(base_url, headers=headers)

        # Initialize services
        self.custom_objects = CustomObjectsService(api.CustomObjectApiClient(http))
        self.custom_object_fields = CustomObjectFieldsService(api.CustomObjectFieldApiClient(http))
        self.custom_object_records = CustomObjectRecordsService(api.CustomObjectRecordApiClient(http))
        self.record_events = RecordEventsService(api.RecordEventApiClient(http))
        self.object_triggers = ObjectTriggersService(api.ObjectTriggerApiClient(http))
        self.record_attachments = RecordAttachmentsService(api.RecordAttachmentApiClient(http))
        self.permission_policies = PermissionPoliciesService(api.PermissionPolicyApiClient(http))
        self.access_rules = AccessRulesService(api.AccessRuleApiClient(http))
