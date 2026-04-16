from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateAddressCmd:
    city: str
    country_code: str
    name: str
    province: str
    street: str
    zip: str
    state: str = ""
    provider_reference: str = ""


@dataclass(frozen=True, slots=True)
class UpdateAddressCmd:
    city: str | None = None
    country_code: str | None = None
    name: str | None = None
    province: str | None = None
    street: str | None = None
    zip: str | None = None
    state: str | None = None
