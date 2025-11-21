from libzapi.domain.models.ticketing.sla_policies import SlaPolicy
from libzapi.infrastructure.serialization.cattrs_converter import get_converter


def to_domain(data: dict) -> SlaPolicy:
    return get_converter().structure(data, SlaPolicy)
