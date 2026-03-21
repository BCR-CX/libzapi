from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateRedirectRuleCmd:
    brand_id: int = 0
    redirect_from: str = ""
    redirect_to: str = ""
    redirect_status: int = 301
