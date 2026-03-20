from libzapi.application.services.agent_availability.availabilities_service import AvailabilitiesService
from libzapi.application.services.agent_availability.capacity_rules_service import CapacityRulesService
from libzapi.application.services.agent_availability.unified_agent_statuses_service import (
    UnifiedAgentStatusesService,
)
from libzapi.application.services.agent_availability.account_group_availability_service import (
    AccountGroupAvailabilityService,
)
from libzapi.application.services.agent_availability.engagements_service import EngagementsService
from libzapi.application.services.agent_availability.queues_service import QueuesService
from libzapi.infrastructure.http.auth import oauth_headers, api_token_headers
from libzapi.infrastructure.http.client import HttpClient
import libzapi.infrastructure.api_clients.agent_availability as api


class AgentAvailability:
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

        self.availabilities = AvailabilitiesService(api.AgentAvailabilityApiClient(http))
        self.capacity_rules = CapacityRulesService(api.CapacityRuleApiClient(http))
        self.unified_agent_statuses = UnifiedAgentStatusesService(api.UnifiedAgentStatusApiClient(http))
        self.account_group_availability = AccountGroupAvailabilityService(api.AccountGroupAvailabilityApiClient(http))
        self.engagements = EngagementsService(api.EngagementApiClient(http))
        self.queues = QueuesService(api.QueueApiClient(http))
